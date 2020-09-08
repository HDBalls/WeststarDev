# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
# from odoo.osv import expression


class WorkOrder(models.TransientModel):
    _name = 'workshop.work.order.task'
    _description = "Create task from workshop service"

    @api.model
    def default_get(self, fields):
        result = super(WorkOrder, self).default_get(fields)

        active_model = self._context.get('active_model')
        if active_model != 'workshop.vehicle.log.services':
            raise UserError(_("You can only apply this action from a service."))

        active_id = self._context.get('active_id')
        if 'service_id' in fields and active_id:
            service = self.env['workshop.vehicle.log.services'].browse(active_id)
            if service.task_id:
                raise UserError(_("The service already has a work order."))
            result['name'] = _('Job Card for ') + service.name
            result['service_id'] = active_id
            result['owner_id'] = service.owner_id.id
        return result

    name = fields.Char()
    service_id = fields.Many2one('workshop.vehicle.log.services', string='Services')
    owner_id = fields.Many2one('res.partner', string='Owner')
    user_id = fields.Many2one('res.users', string='Assigned To', required=1, default=lambda self: self.env.user.id)
    deadline = fields.Date(string='Deadline', index=True, copy=False, tracking=True)
    planned_hours = fields.Float(required=1)

    def action_lost_reason_apply(self):
        task = self._prepare_task()
        # task.action_confirm()
        view_form_id = self.env.ref('project.view_task_form2').id
        action = self.env.ref('project.action_view_task').read()[0]
        action.update({
            'views': [(view_form_id, 'form')],
            'view_mode': 'form',
            'name': task.name,
            'res_id': task.id,
        })
        return action

    def _prepare_task(self):
        # create SO
        task = self.env['project.task'].create({
            'name': self.name,
            # 'partner_id': self.owner_id.id,
            # 'service_id': self.service_id,
            # 'user_id': self.user_id,
            # # 'project_id': self.env['project.project'].search([('name', '=', 'Work Order')]).id,
            # # 'project_id': '10',
            # 'planned_hours': self.planned_hours,
            # 'date_deadline': self.deadline,
            # 'company_id': self.env.company.id,
            # 'analytic_account_id': self.task_id.project_id.analytic_account_id.id,
        })

        task.update({
            'partner_id': self.owner_id.id,
            'service_id': self.service_id,
            'user_id': self.user_id,
            'project_id': self.env['project.project'].search([('name', '=', 'Work Order')]).id,
            # 'project_id': '10',
            'planned_hours': self.planned_hours,
            'date_deadline': self.deadline,
            # 'company_id': self.env.company.id,
        })

        # link service to task
        self.service_id.write({
            'task_id': task.id,
            'state': 'in_progress'
            # 'partner_id': sale_order.partner_id.id,
            # 'email_from': sale_order.partner_id.email,
        })

        return task
