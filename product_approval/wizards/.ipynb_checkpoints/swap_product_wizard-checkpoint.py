# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
# from odoo.osv import expression


class SwapProduct(models.TransientModel):
    _name = 'swap.product.wizard'
    _description = "Swap a product"

    sale_order_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one('product.product')
    optional_product_ids = fields.Many2many('product.template', related='sale_order_id.product_id.optional_product_ids', readonly=True)

    @api.model
    def default_get(self, fields):
        result = super(SwapProduct, self).default_get(fields)

        active_id = self._context.get('active_id')
        if 'sale_order_id' in fields and active_id:
            sale_order_line = self.env['sale.order.line'].browse(active_id)
            if sale_order_line.id:
                result.update({
                    'sale_order_id': sale_order_line and sale_order_line.id or False,
                    'product_id': sale_order_line.product_id and sale_order_line.product_id.id or False
                })

        return result

    def _get_optional_products(self):
        domain = [('id', '=', '-1')]
        optional_product_list = []
        
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        
        if sale_order_line:
            for optional_product_id in sale_order_line.product_id.optional_product_ids:
                 optional_product_list.append(optional_product_id.id)   
                
        if optional_product_list:
            domain = [('id', 'in', optional_product_list)]
            
        return domain
    
    optional_product_id = fields.Many2one('product.template', domain=_get_optional_products, required=True)

    def action_swap_product(self):
        active_id = self.sale_order_id.id
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        
        if sale_order_line:
            sale_id = sale_order_line.order_id.id
            quantity = sale_order_line.product_uom_qty
            
            new_line = self.env['sale.order.line'].create({
                'order_id': sale_id,
                'product_id': self.optional_product_id.product_variant_id.id,
                'name': self.optional_product_id.name,
                'product_uom' : self.optional_product_id.uom_id.id,
                'product_uom_qty': quantity
            })
            
            new_line.product_id_change()
            sale_order_line.unlink()
            