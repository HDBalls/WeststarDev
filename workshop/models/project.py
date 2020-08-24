# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    service_id = fields.Many2one('workshop.vehicle.log.services', 'Service')
    # vehicle_id = fields.Integer('workshop.vehicle', string='Vehicle', related=service_id.vehicle_id, store=True, readonly=True)
