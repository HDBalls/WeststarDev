# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    workshop_employee = fields.Boolean('Workshop Employee')
    
class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    
    workshop_employee = fields.Boolean('Workshop Employee') 