# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
# from odoo.osv import expression


class SwapProduct(models.TransientModel):
    _name = 'swap.product.wizard'
    _description = "Swap a product"

    optional_product_ids = fields.One2many('product.template', 'product_id', related='product_id.optional_product_ids', domain=[('product_id', '=', self.sale_order_id)])

    @api.model
    def default_get(self, fields):
        result = super(SwapProduct, self).default_get(fields)

        # active_model = self._context.get('active_model')
        # if active_model != 'workshop.vehicle.log.services':
        #     raise UserError(_("You can only apply this action from a service."))

        active_id = self._context.get('active_id')
        if 'sale_order_id' in fields and active_id:
            sale_lines = self.env['sale.order.lines'].browse(active_id)
            if sale_lines.id:
                result['sale_order_id'] = active_id

        return result

    sale_order_id = fields.Many2one('sale.order.lines')

