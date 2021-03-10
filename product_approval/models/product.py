from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Product(models.Model):
    _inherit = "product.template"

    alt_product_ids = fields.Many2many('product.template', 'product_approval_product_rel', 'product_template_id', 'product_id')
    # optional_product_ids
