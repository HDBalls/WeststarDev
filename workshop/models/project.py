# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    order_line = fields.One2many('sale.order', 'order_id', string='Order Lines', copy=True,
                                 auto_join=True)
    service_id = fields.Many2one('workshop.vehicle.log.services', 'Service')
    # vehicle_id = fields.Integer('workshop.vehicle', string='Vehicle', related=service_id.vehicle_id, store=True, readonly=True)


class ProjectTaskWorkOrder(models.Model):
    _name = 'project.task.work.order'
    _description = 'Work Order'

    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                               copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one('product.product', 'Product')
    name = fields.Char(related='product_id.name', string='Description')
    quantity = fields.Integer('Quantity')
