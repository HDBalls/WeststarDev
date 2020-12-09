# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_number = fields.Char('Customer Number', readonly=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        if len(vals_list) == 1:
            customer_number = ''
            seq_date = None
            if vals_list[0].get('supplier_rank', 1) == 1:
                customer_number = self.env['ir.sequence'].next_by_code('bluestar.supplier.number.sequence', sequence_date=seq_date) or ''
            else:
                customer_number = self.env['ir.sequence'].next_by_code('bluestar.customer.number.sequence', sequence_date=seq_date) or ''
            vals_list[0]['customer_number'] = customer_number

        partners = super(ResPartner, self).create(vals_list)
        return partners