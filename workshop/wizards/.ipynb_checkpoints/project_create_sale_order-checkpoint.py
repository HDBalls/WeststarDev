# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjectCreateSalesOrder(models.TransientModel):
    _inherit = 'project.create.sale.order'
    
    def action_create_sale_order(self):
        raise UserError('Bitch be humble.')
        super(ProjectCreateSalesOrder, self).action_create_sale_order()
    
    def _make_billable(self, sale_order):
        self._make_billable_line(sale_order)
        if self.billable_type == 'project_rate':
            super(ProjectCreateSalesOrder, self)._make_billable_at_project_rate(sale_order)
        else:
            super(ProjectCreateSalesOrder, self)._make_billable_at_employee_rate(sale_order)
            
    def _make_billable_line(self, sale_order):
        task_id = self.env['project.task'].search([('project_id', '=', self.project_id.id)]).id
        raise UserError(task_id)
        if task_id:
            self._create_parts_item(sale_order, task_id)
            self._create_expenses_item(sale_order, task_id)
            
    def _create_parts_item(self, sale_order, task_id):
        ## Create section in sales Order line
        part_items = task_id.order_line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'dispaly_type': 'line_section',
            'name': 'Parts',
            'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id,
        })
        for part_item in part_items:
            # create SO line
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': part_item.product_id.id,
#                     'price_unit': part_item.price_unit,
                'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id,
                'product_uom_qty': part_item.quantity,
            })
            part_item.write({'external_id':sale_order_line.id})   
            
    def _create_expenses_item(self, sale_order, task_id):
        expenses_items = task_id = task_id.expense_order_line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'dispaly_type': 'line_section',
            'name': 'Expenses',
            'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id,
        })
        for expenses_item in expenses_items:
            # create SO line
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': expenses_item.product_id.id,
#                     'price_unit': part_item.price_unit,
                'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id,
                'product_uom_qty': expenses_item.quantity,
            })
            expenses_item.write({'external_id':sale_order_line.id})  
            
        