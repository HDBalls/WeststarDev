# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjectCreateSalesOrderInherit(models.TransientModel):
    _inherit = 'project.task.create.sale.order'

    #     def action_create_sale_order(self):
    # #         raise UserError('Bitch be humble.')
    #         super(ProjectCreateSalesOrderInherit, self).action_create_sale_order()

    def action_create_sale_order(self):
        sale_order = self._prepare_sale_order()
#         sale_order.action_confirm()
        view_form_id = self.env.ref('sale.view_order_form').id
        action = self.env.ref('sale.action_orders').read()[0]
        action.update({
            'views': [(view_form_id, 'form')],
            'view_mode': 'form',
            'name': sale_order.name,
            'res_id': sale_order.id,
        })
        return action
    
    def _prepare_sale_order(self):
        sale_order = super(ProjectCreateSalesOrderInherit, self)._prepare_sale_order()
        warehouse_id = self.env['stock.warehouse'].search([('name', 'ilike', 'workshop'), ('company_id', '=', self.env.company.id)], limit=1)
        sale_order.write({
            'warehouse_id': warehouse_id,
            'task_id': self.task_id,
            'computer_programming': self.task_id.comp_prog_amount
        })
        sale_order_line = self.env['sale.order.line'].create({
            'sequence': 0,
            'order_id': sale_order.id,
            'display_type': 'line_section',
            'name': 'Labour',
            'project_id': self.task_id.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': self.task_id.id,
        })
        self._make_billable_line(sale_order)
        return sale_order

    def _make_billable_line(self, sale_order):
        if self.task_id:
            self._create_parts_item(sale_order, self.task_id)
            self._create_lubricant_item(sale_order, self.task_id)
            self._create_expenses_item(sale_order, self.task_id)
            self._create_extra_services(sale_order, self.task_id)
            self.task_id.service_id.write({'state': 'awaiting_confirmation'})

    def _create_parts_item(self, sale_order, task_id):
        ## Create section in sales Order line
        part_items = task_id.order_line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'display_type': 'line_section',
            'name': 'Parts',
            'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id.id,
        })
        for part_item in part_items:
            # create SO line
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': part_item.product_id.id,
                #                     'price_unit': part_item.price_unit,
                'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id.id,
                'product_uom_qty': part_item.quantity
            })
            part_item.write({'external_id': sale_order_line.id})

    def _create_expenses_item(self, sale_order, task_id):
        expenses_items = task_id.expense_order_line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'display_type': 'line_section',
            'name': 'Expenses',
            'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id.id,
        })
        for expenses_item in expenses_items:
            # create SO line
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': expenses_item.product_id.id,
#                 'price_unit': expenses_item.price_unit,
                'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id.id,
                'product_uom_qty': expenses_item.quantity,
            })
            expenses_item.write({'external_id': sale_order_line.id})
        
    def _create_lubricant_item(self, sale_order, task_id):
        lubricant_items = task_id.lubricant_order_line
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'display_type': 'line_section',
            'name': 'Lubricants',
            'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id.id,
        })
        for lubricant_item in lubricant_items:
            # create SO line
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': lubricant_item.product_id.id,
#                 'price_unit': lubricant_item.price_unit,
                'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id.id,
                'product_uom_qty': lubricant_item.quantity,
            })
            lubricant_item.write({'external_id': sale_order_line.id})
            
    def _create_extra_services(self, sale_order, task_id):
        Products = self.env['product.product']
        sup_sun = Products.search([('type', '=', 'service'), ('default_code', '=', 'sup_sund')])
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'display_type': 'line_section',
            'name': 'Extra',
            'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
            'task_id': task_id.id,
        })
        if task_id.computer_programming:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': task_id.computer_programming.id,
#                 'price_unit': task_id.comp_prog,
                'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id.id,
                'product_uom_qty': 1,
            })
        if sup_sun:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': sup_sun.id,
                'price_unit': 0.00,
                'project_id': task_id.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': task_id.id,
                'product_uom_qty': 1,
            })

