from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def action_confirm(self):
        sale_order = super(SaleOrder, self).action_confirm()
        if self.tasks_ids:
            for task_id in self.tasks_ids:
                task_id.service_id.write({'state': 'awaiting_parts'})
        return sale_order