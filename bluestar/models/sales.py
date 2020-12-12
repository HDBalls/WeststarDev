# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ref_number = fields.Char('Reference #')

    amount_undiscounted = fields.Monetary('Amount Before Discount', compute='_compute_amount_undiscounted', digits=0)

    @api.onchange('partner_id')
    def onchange_customer_id(self):
        Template = self.env['sale.order.template']
        template = False
        name = self.partner_id.name
        
        if name:
            if 'JULIUS BERGER' in name.upper():
                template = Template.search([('name', 'ilike', 'Julius Berger')], limit = 1)
            else:
                template = Template.search([('name', 'ilike', 'Default')], limit = 1)
        
        if template != False:
            self.update({'sale_order_template_id': template.id})

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    np_number = fields.Char('N/P Number')
    eta = fields.Char('ETA')