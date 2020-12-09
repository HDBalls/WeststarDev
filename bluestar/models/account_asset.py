# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    def validate_asset(self):
        Assets = self.env['account.asset'].search([('state', '=', 'draft')])
        for asset in Assets:
            asset.validate()