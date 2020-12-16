# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ref_number = fields.Char('Reference #')

    amount_undiscounted = fields.Monetary('Amount Before Discount', compute='_compute_amount_undiscounted', digits=0)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    np_number = fields.Char('N/P Number')
    eta = fields.Char('ETA')

