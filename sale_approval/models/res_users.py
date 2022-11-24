# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _

class Users(models.Model):
    _inherit = "res.users"
    
    sale_order_can_approve = fields.Selection(selection_add=[('yes', 'Yes'), ('no', 'No')], 'Can Approve Sale?',default='no', ondelete={'yes': 'set default', 'no':'set default'})
   # sale_order_amount_limit = fields.Float("(SO) Amount Limit", digits=(16, 0), required=True)
    sale_order_discount_limit = fields.Float("(SO) Discount Limit", digits=(16, 0), required=True)



 


















# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
