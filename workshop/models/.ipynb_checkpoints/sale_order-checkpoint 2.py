from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    proforma_invoice_number = fields.Char('PFI NO', readonly=False)
    discount_group_percent = fields.Float('Discount Percentage', store=True)
    computer_programming = fields.Float('Computer Programming', default=0.00, store=True)
    
    @api.onchange('discount_group_percent')
    def update_discount(self):
        SaleLine = self.env['sale.order.line'].search([('product_id.categ_id', 'ilike', 'part')])
        for sale_line in SaleLine:
#             if record.product_id.categ_id == 'Parts Item':
            sale_line.write({'discount': self.discount_group_percent})
    
    def action_confirm(self):
        sale_order = super(SaleOrder, self).action_confirm()
        if self.tasks_ids:
            for task_id in self.tasks_ids:
                task_id.service_id.write({'state': 'awaiting_parts'})
        return sale_order
    
#     def create(self, vals):
#         seq_date = None
# #         if vals.get('proforma_invoice_number', _('New')) == _('New'):
#         vals['proforma_invoice_number'] = self.env['ir.sequence'].next_by_code('workshop.pfi.code.sequence', sequence_date=seq_date) or _('New')

#         result = super(SaleOrder, self).create(vals)
#         return result
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
#     discount_group_percent = fields.Float(related='order_id.discount_group_percent', store=True)
    
#     @api.onchange('discount_group_percent')
#     def update_discount(self):
#         for record in self:
# #             if record.product_id.categ_id == 'Parts Item':
#             record.discount = record.discount_group_percent