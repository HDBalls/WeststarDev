# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProviderBluestar(models.Model):
    _inherit = 'delivery.carrier'
    
    delivery_type = fields.Selection(selection_add=[('bluestar', 'Bluestar')])
    
    def bluestar_rate_shipment(self, order):
        price = 0.00
        CurrencyEUR = self.env['res.currency'].search([('name', 'ilike', 'eur')], limit=1)
        for line in order.order_line:
            weight = line.product_id.weight
            volume = line.product_id.volume
            chargeable_weight = ((volume * 1000) / 6)
            
            if weight > chargeable_weight:
                chargeable_weight = weight
                
            price += self._get_price_by_weight(chargeable_weight, volume, CurrencyEUR) * line.product_uom_qty
            
        return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': False}    
            
    def _get_price_by_weight(self, chargeable_weight, volume, currency):
        rate_to_naira = (1 / currency.rate)
        if self.product_id.default_code == 'Delivery_Air':
            return chargeable_weight + (rate_to_naira * 12)
        elif self.product_id.default_code == 'Delivery_Sea':
            return (volume * 225)
        
        return 0.00
