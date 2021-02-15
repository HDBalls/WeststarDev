from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.AbstractModel):
    _name = 'report.workshop.workshop_account_invoice'
    _description = 'Invoice Report'
    
    def get_sales_order(self, order_number):
        SalesOrder = self.env['sale.order'].search([('name', '=', order_number)], limit=1)
        return SalesOrder
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
#         if not data.get('form'):
#             raise UserError(_("Form content is missing, this report cannot be printed."))
            
        return {
            'doc_ids': docids,
            'doc_model': 'aacount.move',
            'docs': self.env['account.move'].browse(docids),
            'data': data,
            'sale_order': self.get_sales_order,

        }