from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.AbstractModel):
    _name = 'report.workshop.workshop_account_invoice_3'
    _description = 'Invoice Report'
    
    def get_sales_order(self, order_number):
        SalesOrder = self.env['sale.order'].search([('name', '=', order_number)], limit=1)
        return SalesOrder
    
    def get_total(self, account_id):
        params = [account_id]
        query = """SELECT PC.NAME, SUM(aml.price_subtotal) as SUBTOTAL FROM ACCOUNT_MOVE_LINE aml
        INNER JOIN PRODUCT_TEMPLATE pt ON pt.ID = (SELECT product_tmpl_id FROM PRODUCT_PRODUCT WHERE ID = aml.PRODUCT_ID)
        INNER JOIN PRODUCT_CATEGORY pc ON pc.ID = pt.CATEG_ID
        WHERE aml.MOVE_ID = %s
        GROUP BY PC.NAME"""
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res
    
    def total(self, account_id):
        total = {}
        for sale in self.get_total(account_id):
            total[sale['name']] = sale['subtotal']
        return total
    
    @api.model
    def _get_report_values(self, docids, data=None):
            
        return {
            'doc_ids': docids,
            'doc_model': 'aacount.move',
            'docs': self.env['account.move'].browse(docids),
            'data': data,
            'total': self.total,
            'sale_order': self.get_sales_order,
        }