from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.AbstractModel):
    _name = 'report.bluestar.report_bluestar_saleorder_jbn_document'
    _description = 'Proforma Invoice JBN'
    
    def get_total(self, order_id):
        params = [order_id]
        query = """SELECT pc.NAME, SUM(sol.price_subtotal) as SUBTOTAL FROM SALE_ORDER_LINE sol
        INNER JOIN PRODUCT_TEMPLATE pt ON pt.ID = (SELECT product_tmpl_id FROM PRODUCT_PRODUCT WHERE ID = sol.PRODUCT_ID)
        INNER JOIN PRODUCT_CATEGORY pc ON pc.ID = pt.CATEG_ID
        WHERE sol.ORDER_ID = %s
        GROUP BY pc.NAME"""
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res
    
    def total(self, order_id):
        total = {}
        for sale in self.get_total(order_id):
            total[sale['name']] = sale['subtotal']
        return total
    
    @api.model
    def _get_report_values(self, docids, data=None):
            
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': self.env['sale.order'].browse(docids),
            'data': data,
            'total': self.total,
        }