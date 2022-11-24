# -*- coding: utf-8 -*-

from odoo import models, fields, api



class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    base = fields.Selection(selection_add=[('gross_price', 'Base List Price')])
