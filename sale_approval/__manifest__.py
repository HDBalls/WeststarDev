# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quotations/Sales Orders Approval',
    'version': '13.0',
    'category': 'Sales',
    'author': 'PPTS',
    'sequence': 15,
    'summary': 'Quotations/Sales Orders Approval',
    'description': """
Manage sales quotations and orders Approval.
    """,
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'https://www.pptssolutions.com',
    'license': 'LGPL-3',
    'support': 'business@pptservices.com',
    'depends': ['base_setup', 'sale', 'sales_team'],
	'installable': False,
    'auto_install': False,
    'application': False,
    'data': [
        'data/mail_template.xml',
        'wizard/sale_approval_reason_view.xml',
        'views/res_user_views.xml',
        'views/sale_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
}
