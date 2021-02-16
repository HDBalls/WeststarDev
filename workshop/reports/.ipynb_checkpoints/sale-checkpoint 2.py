from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError

class Sale(models.AbstractModel):
    _name = 'report.workshop.workshop_estimate_invoice'
    _description = 'Workshop Estimate Report'
    
    def get_total(self, sale_order_id):
        params = [sale_order_id]
        query = """SELECT PC.NAME, SUM(sol.price_subtotal) as SUBTOTAL FROM SALE_ORDER_LINE sol
        INNER JOIN PRODUCT_TEMPLATE pt ON pt.ID = (SELECT product_tmpl_id FROM PRODUCT_PRODUCT WHERE ID = sol.PRODUCT_ID)
        INNER JOIN PRODUCT_CATEGORY pc ON pc.ID = pt.CATEG_ID
        WHERE sol.ORDER_ID = %s
        GROUP BY PC.NAME"""
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res
    
    def total(self, sale_order_id):
        total = {}
        for sale in self.get_total(sale_order_id):
            total[sale['name']] = sale['subtotal']
        return total
    
    def save(self, order_id, total = 0.00):
        SaleOrder = self.env['sale.order.line'].search([('order_id', '=', order_id), ('product_id.default_code', '=', 'sup_sund')]) 
        if SaleOrder:
            SaleOrder.write({'price_unit': total})
    
    @api.model
    def _get_report_values(self, docids, data=None):
            
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': self.env['sale.order'].browse(docids),
            'data': data,
            'total': self.total,
            'save': self.save

        }