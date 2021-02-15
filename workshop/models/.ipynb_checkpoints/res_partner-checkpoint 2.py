# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    service_id = fields.One2many('workshop.vehicle.log.services', 'owner_id', 'Diagnosis')
    
    def action_workshop_services(self):
        self.ensure_one()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Diagnosis',
            'view_mode': 'tree',
            'res_model': 'workshop.vehicle.log.services',
            'domain': [('owner_id', '=', self.id)],
            'context': "{'create': True}"
        }
            