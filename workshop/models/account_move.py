# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        account = super(AccountMove, self).action_post()
        sale = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
        if sale:
            if sale.task_id:
                sale.task_id.service_id.write({'state': 'awaiting_payment'})
        return account