# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('confirmation', 'Confirm Approval'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    # def button_approve(self, force=False):
    #     self.write({'approver_id': '', 'state': 'confirmation', 'date_approve': fields.Date.context_today(self)})
    #     # self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
    #     return {}

    def button_confirm_approval(self, force=False):
        for purchase in self:
            purchase.state = 'confirmation'
        # self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
        # self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        # return {}
     
    def button_confirm_order(self, force=False):
        for purchase in self:
            purchase.state = 'to approve'

    @api.model
    def _getUserGroupId(self):
        return [('groups_id', '=', self.env.ref('purchase.group_purchase_manager').id)]

    approver_id = fields.Many2one(
        string='Approver', domain=_getUserGroupId, readonly=True)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
