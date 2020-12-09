from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError
import re

class SaleOrder(models.AbstractModel):
    _name = 'report.bluestar.report_bluestar_for_jbn_saleorder'
    _description = 'Proforma Invoice JBN'
    
    def get_total_by_product_categories(self, order_id):
        params = [order_id]
        query = """SELECT pc.NAME, SUM(sol.price_subtotal) as SUBTOTAL FROM SALE_ORDER_LINE sol
        INNER JOIN PRODUCT_TEMPLATE pt ON pt.ID = (SELECT product_tmpl_id FROM PRODUCT_PRODUCT WHERE ID = sol.PRODUCT_ID)
        INNER JOIN PRODUCT_CATEGORY pc ON pc.ID = pt.CATEG_ID
        WHERE sol.ORDER_ID = %s
        GROUP BY pc.NAME"""
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res
    
    def total_by_product_categories(self, order_id):
        total = {}
        for sale_order_line in self.get_total_by_product_categories(order_id):
            total[sale_order_line['name']] = sale_order_line['subtotal']
        return total
    
    def get_discount_total(self, order_id):
        params = [order_id]
        query = """SELECT pc.NAME AS CATEG_NAME, sol.NAME, SUM(sol.price_subtotal) as SUBTOTAL FROM SALE_ORDER_LINE sol
        INNER JOIN PRODUCT_TEMPLATE pt ON pt.ID = (SELECT product_tmpl_id FROM PRODUCT_PRODUCT WHERE ID = sol.PRODUCT_ID)
        INNER JOIN PRODUCT_CATEGORY pc ON pc.ID = pt.CATEG_ID
        WHERE sol.ORDER_ID = %s AND PC.NAME = 'Discount'
        GROUP BY pc.NAME, sol.NAME"""
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        
        discount = {}
        for sale_order_line in res:
            name = sale_order_line['name']
            dicount_perc = re.findall('\d*%', name)
            amount = sale_order_line['subtotal']
            discount['percentage'] = dicount_perc[0]
            discount['amount'] = amount
            
        return discount
    
    @api.model
    def _get_report_values(self, docids, data=None):
            
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': self.env['sale.order'].browse(docids),
            'data': data,
            'total': self.total_by_product_categories,
            'discount_price': self.get_discount_total
        }