# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    order_line = fields.One2many('project.task.work.order.parts', 'order_id', string='Parts', domain="[('product_type', '=', 'product')]")
    expense_order_line = fields.One2many('project.task.work.order.expenses', 'order_id', string='Travel Expenses', domain="[('product_type', '=', 'service'), ('product_category','ilike','expenses')]")
    lubricant_order_line = fields.One2many('project.task.work.order.lubricant', 'order_id', string='Lubricants', domain="[('product_type', '=', 'product')]")
    service_id = fields.Many2one('workshop.vehicle.log.services', 'Service')
    vehicle_id = fields.Many2one('workshop.vehicle', related='service_id.vehicle_id', string='Vehicle') 
    computer_programming = fields.Many2one('product.product', domain=[('type', '=', 'service'), ('default_code', '=', 'comp_prog')])
    comp_prog_amount = fields.Float(string='Programming Amount', store=False, related='computer_programming.list_price')
    
    # vehicle_id = fields.Integer('workshop.vehicle', string='Vehicle', related=service_id.vehicle_id, store=True, readonly=True)
    
#     def create(self, vals):
#         sale_order_id = self.sale_order_id
#         SalesOrderItem = self.env['sale.order.item']
#         sale_item = SalesOrderItem.search[('order_id', '=', sale_order_id)]
#         for line_id in order_item:
#             if sale_item:
#                 sale_item = SalesOrderItem.search[('order_id', '=', sale_order_id)]
#                 value = {
#                     'order_id': sale_order_id,
#                     'product_id': line_id.product_id,
#                     'quantity': line_id.quantity
#                 }
#                 sale_item.create(value)
        
#         result = super(ProjectTask, self).create(vals)
#         return result
        
    @api.onchange('computer_programming')
    def computer_programming_update(self):
        if self.sale_order_id:
            SaleOrderLine = self.env['sale.order.line']
            
            comp_prog = SaleOrderLine.search([('order_id', '=', self.sale_order_id.id),('product_id.type', '=', 'service'), 
                                              ('product_id.default_code', '=', 'comp_prog')], limit = 1)
#             sale_line = SaleOrderLine.search[('display_type', '=', 'line_section'), ('name', '=', 'Parts')]
#             if sale_line:
            if comp_prog:
                if not comp_prog.product_id.id == self.computer_programming.id:
#                     value = {
#                         'order_id': self.sale_order_id.id,
#                         'sequence': comp_prog.sequence,
#                         'product_id': self.computer_programming.id
#                     }
#                     comp_prog.unlink()
#                     sale_line = SaleOrderLine.create(value)
                    comp_prog.write({'product_id':self.computer_programming.id})
            else:
                value = {
                    'order_id': self.sale_order_id.id,
                    'product_id': self.computer_programming.id
                }
                sale_line = SaleOrderLine.create(value)
    
    def action_update_sales_order(self):
        task_id = self.env.context.get('fsm_task_id')
        if task_id:
            task = self.env['project.task'].browse(task_id)

            # don't add material on confirmed SO to avoid inconsistence with the stock picking
            if task.fsm_done:
                return False

            # project user with no sale rights should be able to add materials
            SaleOrderLine = self.env['sale.order.line']
            if self.user_has_groups('project.group_project_user'):
                task = task.sudo()
                SaleOrderLine = SaleOrderLine.sudo()
                
            for order_item in order_line:
                sale_line = SaleOrderLine.search([('order_id', '=', task.sale_order_id.id), ('product_id', '=', order_item.product_id)], limit=1)
                
                if sale_line:
                    vals = {
                        'product_uom_qty': order_item.quantity
                    }
                    if sale_line.qty_delivered_method == 'manual':
                        vals['qty_delivered'] = order_item.quantity
                    sale_line.with_context(fsm_no_message_post=True).write(vals)
                else:
                    vals = {
                        'order_id': task.sale_order_id.id,
                        'product_id': order_item.product_id,
                        'product_uom_qty': order_item.quantity,
#                         'product_uom': self.uom_id.id,
                    }
                    if self.service_type == 'manual':
                        vals['qty_delivered'] = order_item.quantity

                    # Note: force to False to avoid changing planned hours when modifying product_uom_qty on SOL
                    # for materials. Set the current task for service to avoid re-creating a task on SO cnofirmation.
                    if self.type == 'service':
                        vals['task_id'] = task_id
                    else:
                        vals['task_id'] = False

                    sale_line = SaleOrderLine.create(vals)

#             sale_line = SaleOrderLine.search([('order_id', '=', task.sale_order_id.id), ('product_id', '=', self.order_line.product_id)], limit=1)

#             if sale_line:  # existing line: increment ordered qty (and delivered, if delivered method)
#                 vals = {
#                     'product_uom_qty': self.order_line.quantity
#                 }
#                 if sale_line.qty_delivered_method == 'manual':
#                     vals['qty_delivered'] = self.order_line.quantity
#                 sale_line.with_context(fsm_no_message_post=True).write(vals)
#             else:  # create new SOL
#                 vals = {
#                     'order_id': task.sale_order_id.id,
#                     'product_id': self.id,
#                     'product_uom_qty': 1,
#                     'product_uom': self.uom_id.id,
#                 }
#                 if self.service_type == 'manual':
#                     vals['qty_delivered'] = 1

#                 # Note: force to False to avoid changing planned hours when modifying product_uom_qty on SOL
#                 # for materials. Set the current task for service to avoid re-creating a task on SO cnofirmation.
#                 if self.type == 'service':
#                     vals['task_id'] = task_id
#                 else:
#                     vals['task_id'] = False

#                 sale_line = SaleOrderLine.create(vals)

        return True

class ProjectTaskWordOrderLines(models.Model):
    _name = 'project.task.work.order.lines'
    

class ProjectTaskWorkOrderParts(models.Model):
    _name = 'project.task.work.order.parts'

    order_id = fields.Many2one('project.task', string='Order Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one('product.product', 'Product', required=True)
    name = fields.Char(related='product_id.name', string='Description')
    quantity = fields.Integer('Quantity')
    product_type = fields.Char()
    product_category = fields.Many2one('product.category', related='product_id.categ_id')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    external_id = fields.Char()
    
    @api.model
    def create(self, vals):
        task = self.env['project.task'].browse(vals['order_id'])
        if task.sale_order_id:
            SaleOrderLine = self.env['sale.order.line']
#             sale_line = SaleOrderLine.search[('display_type', '=', 'line_section'), ('name', '=', 'Parts')]
#             if sale_line:
            value = {
                'order_id': task.sale_order_id.id,
                'sequence': vals['sequence'],
                'product_id': vals['product_id'],
                'product_uom_qty': vals['quantity'],
            }
            sale_line = SaleOrderLine.create(value)
            vals['external_id'] = sale_line.id
        result = super(ProjectTaskWorkOrderParts, self).create(vals)
        return result

    def unlink(self):
        SaleOrderLine = self.env['sale.order.line']
        for order_line in self:
            if order_line.external_id:
                sale_line = SaleOrderLine.search([('id', '=', order_line.external_id)])
                sale_line.unlink()
        return super(ProjectTaskWorkOrderParts, self).unlink()
    
class ProjectTaskWorkOrderExpenses(models.Model):
    _name = 'project.task.work.order.expenses'
    _description = 'Work Order Expenses'

    order_id = fields.Many2one('project.task', string='Order Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one('product.product', 'Product', required=True, domain=[('type','=','service'), ('categ_id','ilike','expenses')])
    name = fields.Char(related='product_id.name', string='Description')
    quantity = fields.Integer('Quantity')
    product_type = fields.Char()
    product_category = fields.Many2one('product.category', related='product_id.categ_id')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    external_id = fields.Char()

    @api.model
    def create(self, vals):
        task = self.env['project.task'].browse(vals['order_id'])
        if task.sale_order_id:
            SaleOrderLine = self.env['sale.order.line']
#             sale_line = SaleOrderLine.search[('display_type', '=', 'line_section'), ('name', '=', 'Parts')]
#             if sale_line:
            value = {
                'order_id': task.sale_order_id.id,
                'sequence': vals['sequence'],
                'product_id': vals['product_id'],
                'product_uom_qty': vals['quantity'],
                'price_unit': vals['price_unit']
            }
            sale_line = SaleOrderLine.create(value)
            vals['external_id'] = sale_line.id
        result = super(ProjectTaskWorkOrderExpenses, self).create(vals)
        return result

    def unlink(self):
        SaleOrderLine = self.env['sale.order.line']
        for order_line in self:
            if order_line.external_id:
                sale_line = SaleOrderLine.search([('id', '=', order_line.external_id)])
                sale_line.unlink()
        return super(ProjectTaskWorkOrderExpenses, self).unlink()
    
class ProjectTaskWorkOrderLubricant(models.Model):
    _name = 'project.task.work.order.lubricant'
    _description = 'Work Order Expenses'

    order_id = fields.Many2one('project.task', string='Order Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one('product.product', 'Product', required=True, domain=[('type','=','product'), ('categ_id','ilike','workshop')])
    name = fields.Char(related='product_id.name', string='Description')
    quantity = fields.Integer('Liters')
    product_type = fields.Char()
    product_category = fields.Many2one('product.category', related='product_id.categ_id')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    external_id = fields.Char()

    @api.model
    def create(self, vals):
        task = self.env['project.task'].browse(vals['order_id'])
        if task.sale_order_id:
            SaleOrderLine = self.env['sale.order.line']
#             sale_line = SaleOrderLine.search[('display_type', '=', 'line_section'), ('name', '=', 'Parts')]
#             if sale_line:
            value = {
                'order_id': task.sale_order_id.id,
                'sequence': vals['sequence'],
                'product_id': vals['product_id'],
                'product_uom_qty': vals['quantity'],
                'price_unit': vals['price_unit']
            }
            sale_line = SaleOrderLine.create(value)
            vals['external_id'] = sale_line.id
        result = super(ProjectTaskWorkOrderLubricant, self).create(vals)
        return result

    def unlink(self):
        SaleOrderLine = self.env['sale.order.line']
        for order_line in self:
            if order_line.external_id:
                sale_line = SaleOrderLine.search([('id', '=', order_line.external_id)])
                sale_line.unlink()
        return super(ProjectTaskWorkOrderLubricant, self).unlink()