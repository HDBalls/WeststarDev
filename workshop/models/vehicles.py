# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression


class Vehicle(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'workshop.vehicle'
    _description = 'Vehicle'
    _order = 'license_plate asc, acquisition_date asc'

    def _get_default_state(self):
        state = self.env.ref('workshop.workshop_vehicle_state_registered', raise_if_not_found=False)
        return state if state and state.id else False

    name = fields.Char(compute="_compute_vehicle_name", store=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    license_plate = fields.Char(tracking=True,
        help='License plate number of the vehicle (i = plate number for a car)')
    vin_sn = fields.Char('Vin Number', help='Unique number written on the vehicle motor (VIN/SN number)', copy=False)
    engine_no = fields.Char('Engine Number', help='Engine number of the vehicle', copy=False)
    driver_id = fields.Many2one('res.partner', 'Owner', tracking=True, help='Owner of the vehicle', copy=False)
    model_id = fields.Many2one('fleet.vehicle.model', 'Model',
        tracking=True, required=True, help='Model of the vehicle')
    manager_id = fields.Many2one('res.users', related='model_id.manager_id')
    brand_id = fields.Many2one('fleet.vehicle.model.brand', 'Brand', related="model_id.brand_id", store=True, readonly=False)
    # log_drivers = fields.One2many('workshop.vehicle.assignation.log', 'vehicle_id', string='Assignation Logs')
    # log_fuel = fields.One2many('workshop.vehicle.log.fuel', 'vehicle_id', 'Fuel Logs')
    # log_services = fields.One2many('workshop.vehicle.log.services', 'vehicle_id', 'Services Logs')
#     log_contracts = fields.One2many('workshop.vehicle.log.contract', 'vehicle_id', 'Contracts')
#     cost_count = fields.Integer(compute="_compute_count_all", string="Costs")
#     contract_count = fields.Integer(compute="_compute_count_all", string='Contract Count')
    service_count = fields.Integer(compute="_compute_count_all", string='Services')
#     fuel_logs_count = fields.Integer(compute="_compute_count_all", string='Fuel Log Count')
    odometer_count = fields.Integer(compute="_compute_count_all", string='Odometer')
#     history_count = fields.Integer(compute="_compute_count_all", string="Drivers History Count")
    total_amount = fields.Monetary(compute="_calculate_total", string="Total Amount")
    next_assignation_date = fields.Date('Assignation Date', help='This is the date at which the car will be available, if not set it means available instantly')
    acquisition_date = fields.Date('Immatriculation Date', required=False,
        default=fields.Date.today, help='Date when the vehicle has been immatriculated')
#     first_contract_date = fields.Date(string="First Contract Date", default=fields.Date.today)
    color = fields.Char(help='Color of the vehicle')
    state_id = fields.Many2one('workshop.vehicle.state', 'State',
        default=_get_default_state, group_expand='_read_group_stage_ids',
        tracking=True,
        help='Current state of the vehicle', ondelete="set null")
    location = fields.Char(help='Location of the vehicle (garage, ...)')
    seats = fields.Integer('Seats Number', help='Number of seats of the vehicle')
    model_year = fields.Char('Model Year', help='Year of the model')
    doors = fields.Integer('Doors Number', help='Number of doors of the vehicle', default=5)
    tag_ids = fields.Many2many('workshop.vehicle.tag', 'workshop_vehicle_vehicle_tag_rel', 'vehicle_tag_id', 'tag_id', 'Tags', copy=False)
    odometer = fields.Float(compute='_get_odometer', inverse='_set_odometer', string='Last Odometer',
        help='Odometer measure of the vehicle at the moment of this log')
    odometer_unit = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles')
        ], 'Odometer Unit', default='kilometers', help='Unit of the odometer ', required=True)
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle')
    fuel_type = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('lpg', 'LPG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
        ], 'Fuel Type', help='Fuel Used by the vehicle')
    horsepower = fields.Integer()
    horsepower_tax = fields.Float('Horsepower Taxation')
    power = fields.Integer('Power', help='Power in kW of the vehicle')
    co2 = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle')
    image_128 = fields.Image(related='model_id.image_128', readonly=False)
#     contract_renewal_due_soon = fields.Boolean(compute='_compute_contract_reminder', search='_search_contract_renewal_due_soon',
#         string='Has Contracts to renew', multi='contract_info')
#     contract_renewal_overdue = fields.Boolean(compute='_compute_contract_reminder', search='_search_get_overdue_contract_reminder',
#         string='Has Contracts Overdue', multi='contract_info')
#     contract_renewal_name = fields.Text(compute='_compute_contract_reminder', string='Name of contract to renew soon', multi='contract_info')
#     contract_renewal_total = fields.Text(compute='_compute_contract_reminder', string='Total of contracts due or overdue minus one',
#         multi='contract_info')
    car_value = fields.Float(string="Catalog Value (VAT Incl.)", help='Value of the bought vehicle')
    net_car_value = fields.Float(string="Purchase Value", help="Purchase Value of the car")
    residual_value = fields.Float()
    total = fields.Float()
    plan_to_change_car = fields.Boolean(related='driver_id.plan_to_change_car', store=True, readonly=False)

    @api.depends('model_id.brand_id.name', 'model_id.name', 'license_plate')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = (record.model_id.brand_id.name or '') + '/' + (record.model_id.name or '') + '/' + (
                        record.license_plate or _('No Plate'))

    def _get_odometer(self):
        VehicalOdometer = self.env['workshop.vehicle.odometer']
        for record in self:
            vehicle_odometer = VehicalOdometer.search([('vehicle_id', '=', record.id)], limit=1, order='value desc')
            if vehicle_odometer:
                record.odometer = vehicle_odometer.value
            else:
                record.odometer = 0

    def _set_odometer(self):
        for record in self:
            if record.odometer:
                date = fields.Date.context_today(record)
                data = {'value': record.odometer, 'date': date, 'vehicle_id': record.id}
                self.env['workshop.vehicle.odometer'].create(data)
                
    def _calculate_total(self):
        self.total_amount = 0
        self.total = 0
        Cost = self.env['workshop.vehicle.cost']
        Services = self.env['workshop.vehicle.log.services']
#         for record in self:
# #             costs = Cost.search([('vehicle_id', '=', record.id)])
#             services = Services.search([('vehicle_id', '=', record.id)])
#             for service in services:
#                 record.total_amount += (service.amount + service.comp_prog_amount) 
#                 record.total = record.total_amount

    def _compute_count_all(self):
        Odometer = self.env['workshop.vehicle.odometer']
        # LogFuel = self.env['fleet.vehicle.log.fuel']
        LogService = self.env['workshop.vehicle.log.services']
        # LogContract = self.env['fleet.vehicle.log.contract']
        # Cost = self.env['fleet.vehicle.cost']
        for record in self:
            record.odometer_count = Odometer.search_count([('vehicle_id', '=', record.id)])
            # record.fuel_logs_count = LogFuel.search_count([('vehicle_id', '=', record.id)])
            record.service_count = LogService.search_count([('vehicle_id', '=', record.id)])
            # record.contract_count = LogContract.search_count([('vehicle_id', '=', record.id), ('state', '!=', 'closed')])
            # record.cost_count = Cost.search_count([('vehicle_id', '=', record.id), ('parent_id', '=', False)])
            # record.history_count = self.env['workshop.vehicle.assignation.log'].search_count([('vehicle_id', '=', record.id)])

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['workshop.vehicle.state'].search([], order=order)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('driver_id.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('workshop', xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False


class VehicleState(models.Model):
    _name = 'workshop.vehicle.state'
    _order = 'sequence asc'
    _description = 'Vehicle Status'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Used to order the note stages")

    _sql_constraints = [('workshop_state_name_unique', 'unique(name)', 'State name already exists')]


class VehicleOdometer(models.Model):
    _name = 'workshop.vehicle.odometer'
    _description = 'Odometer log for a vehicle'
    _order = 'date desc'

    name = fields.Char(compute='_compute_vehicle_log_name', store=True)
    date = fields.Date(default=fields.Date.context_today)
    value = fields.Float('Odometer Value', group_operator="max")
    vehicle_id = fields.Many2one('workshop.vehicle', 'Vehicle', required=True)
    unit = fields.Selection(related='vehicle_id.odometer_unit', string="Unit", readonly=True)
    driver_id = fields.Many2one(related="vehicle_id.driver_id", string="Driver", readonly=False)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    @api.depends('vehicle_id', 'date')
    def _compute_vehicle_log_name(self):
        for record in self:
            name = record.vehicle_id.name
            if not name:
                name = str(record.date)
            elif record.date:
                name += ' / ' + str(record.date)
            record.name = name

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.unit = self.vehicle_id.odometer_unit                                              


class VehicleTag(models.Model):
    _name = 'workshop.vehicle.tag'
    _description = 'Vehicle Tag'

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists !")]


class VehicleServiceType(models.Model):
    _name = 'workshop.service.type'
    _description = 'Workshop Service Type'

    name = fields.Char(required=True, translate=True)
    category = fields.Selection(selection_add=[
        ('contract', 'Contract'),
        ('service', 'Service')
        ], 'Category', required=True, default='contract', ondelete={'contract': 'set default', 'service':'set default'}, help='Choose whether the service refer to contracts, vehicle services or both')