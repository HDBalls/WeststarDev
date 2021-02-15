# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
#     employee_id = fields.Many2one('hr.employee', "Employee", check_company=True, domain=[('workshop_employee', '!=', False)])