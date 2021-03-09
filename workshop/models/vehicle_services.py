# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta


class WorkshopVehicleCost(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'workshop.vehicle.cost'
    _description = 'Cost related to a vehicle'
    _order = 'date desc, vehicle_id asc'

    name = fields.Char(related='vehicle_id.name', string='Name', store=True, readonly=False)
    code = fields.Char(store=True, readonly=False)
    owner_id = fields.Many2one('res.partner', related='vehicle_id.driver_id', string='Owner', store=True, readonly=True)
    vehicle_id = fields.Many2one('workshop.vehicle', 'Vehicle', required=True, help='Vehicle concerned by this log')
    cost_subtype_id = fields.Many2one('workshop.service.type', 'Type', help='Cost type purchased with this cost')
    amount = fields.Monetary('Total Price')
    cost_type = fields.Selection([
        ('contract', 'Contract'),
        ('services', 'Services'),
        ('fuel', 'Fuel'),
        ('other', 'Other')
        ], 'Category of the cost', default="other", help='For internal purpose only', required=True)

    operation_type = fields.Selection([
        ('action_taken', 'Action Taken'),
        ('complaint', 'Customers Complaint'),
        ('diagnosis', 'Diagnostic Finding')
    ])
    parent_id = fields.Many2one('workshop.vehicle.cost', 'Parent', help='Parent cost to this current cost')
    cost_ids = fields.One2many('workshop.vehicle.cost', 'parent_id', 'Included Services', copy=True)
    odometer_id = fields.Many2one('workshop.vehicle.odometer', 'Odometer', help='Odometer measure of the vehicle at the moment of this log')
    odometer = fields.Float(compute="_get_odometer", inverse='_set_odometer', string='Odometer Value',
        help='Odometer measure of the vehicle at the moment of this log')
    odometer_unit = fields.Selection(related='vehicle_id.odometer_unit', string="Unit", readonly=True)
    date = fields.Date(help='Date when the cost has been executed')
    # contract_id = fields.Many2one('fleet.vehicle.log.contract', 'Contract', help='Contract attached to this cost')
    auto_generated = fields.Boolean('Automatically Generated', readonly=True)
    description = fields.Char("Cost Description")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def _get_odometer(self):
        self.odometer = 0.0
        for record in self:
            record.odometer = False
            if record.odometer_id:
                record.odometer = record.odometer_id.value

    def _set_odometer(self):
        for record in self:
            if not record.odometer:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            odometer = self.env['workshop.vehicle.odometer'].create({
                'value': record.odometer,
                'date': record.date or fields.Date.context_today(record),
                'vehicle_id': record.vehicle_id.id
            })
            self.odometer_id = odometer

    @api.model_create_multi
    def create(self, vals_list):
        for data in vals_list:
            # make sure that the data are consistent with values of parent and contract records given
            if 'parent_id' in data and data['parent_id']:
                parent = self.browse(data['parent_id'])
                data['vehicle_id'] = parent.vehicle_id.id
                data['date'] = parent.date
                data['cost_type'] = parent.cost_type
                data['code'] = self.env['ir.sequence'].next_by_code('workshop.job.card.operation.code.sequence', sequence_date=None) or _('New')
            # if 'contract_id' in data and data['contract_id']:
                # contract = self.env['workshop.vehicle.log.contract'].browse(data['contract_id'])
                # data['vehicle_id'] = contract.vehicle_id.id
                # data['cost_subtype_id'] = contract.cost_subtype_id.id
                # data['cost_type'] = contract.cost_type
            if 'odometer' in data and not data['odometer']:
                # if received value for odometer is 0, then remove it from the
                # data as it would result to the creation of a
                # odometer log with 0, which is to be avoided
                del data['odometer']
        return super(WorkshopVehicleCost, self).create(vals_list)


class WorkshopVehicleLogServices(models.Model):
    _name = 'workshop.vehicle.log.services'
    _inherits = {'workshop.vehicle.cost': 'cost_id'}
    _description = 'Services for vehicles'

    @api.model
    def default_get(self, default_fields):
        res = super(WorkshopVehicleLogServices, self).default_get(default_fields)
        service = self.env.ref('workshop.type_service_service_8', raise_if_not_found=False)
        res.update({
            'date': fields.Date.context_today(self),
            'date_in': fields.Date.context_today(self),
            'cost_subtype_id': service and service.id or False,
            'cost_type': 'services'
        })
        return res
    name = fields.Char(string='Job Card #', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    task_id = fields.Many2one('project.task', 'Work Order')
    sale_order_id = fields.Many2one('sale.order', 'Sales Order', related='task_id.sale_order_id')
    date_in = fields.Date(help='The date the vehicle was brought into the workshop', store=True)
    date_out = fields.Date(help='The date the vehicle left the workshop', store=True)
    project_id = fields.Many2one('project.project', string='Nature Of Job', required=True, domain=[('name', 'in', ['In Workshop Service', 'Field Service'])])
    received_by = fields.Many2one('res.user')
    brought_in_by = fields.Many2one('res.partner')
    date_deadline = fields.Date(string='Deadline', readonly=False)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('awaiting_confirmation', 'Awaiting Confirmation'),
        ('awaiting_parts', 'Awaiting Parts'),
        ('in_progress', 'Repair In Progress'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('done', 'Complete'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='pending')
    fuel_log = fields.Selection([
        ('empty', 'Empty'),
        ('one_half', 'One Half'),
        ('one_quarter', 'One Quarter'),
        ('three_quarter', 'Three Quarter'),
        ('half', 'Half Full'),
        ('full', 'Full')
    ], string='Fuel')
    # vendor_id = fields.Many2one('res.partner', 'Vendor')
    # we need to keep this field as a related with store=True because the graph view doesn't support
    # (1) to address fields from inherited table and (2) fields that aren't stored in database
    amount = fields.Monetary('Total Price', compute='_calculate_total')
    cost_amount = fields.Float(related='task_id.material_line_total_price', string='Amount', store=True, readonly=True)
    notes = fields.Text()
    cost_id = fields.Many2one('workshop.vehicle.cost', 'Cost', required=True, ondelete='cascade')

    def _calculate_total(self):
#         Invoices = self.env['account.move']
#         Sales = self.env['sale.order']
        for record in self:
#             sale = Sales.search([('id', '=', record.task_id.sale_order_id)])
            record.amount = record.cost_amount
            for cost in record.cost_ids:
                record.amount = record.amount + cost.amount 
#             invoices = Invoices.search((['sale_order_id', '=', record.task_id.sale_order_id]))
#             if invoices:
#                 for invoice in invoices:

    def workshop_action_parts(self):
        self.write({'state': 'in_progress'})
    
    def workshop_action_payment(self):
        self.write({'state': 'done'}) 
        
    def action_in_progress(self):
        return self.write({'state': 'in_progress'})

    def action_done(self):
        return self.write({'state': 'done'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    @api.onchange('task_id.material_line_total_price')
    def _onchange_cost_amount(self):
        self.amount = self.cost_amount

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.odometer_unit = self.vehicle_id.odometer_unit
            self.owner_id = self.vehicle_id.driver_id.id

    @api.model
    def create(self, vals):

        seq_date = None
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('workshop.job.card.sequence', sequence_date=seq_date) or _('New')

        result = super(WorkshopVehicleLogServices, self).create(vals)
        return result

    def action_view_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "views": [[False, "form"]],
            "res_id": self.task_id.id,
            "context": {"create": False, "show_sale": True},
        }
