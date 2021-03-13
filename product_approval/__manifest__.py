# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Approval',
    'version': '13.0',
    'category': 'Inventory',
    'author': 'PPTS',
    'sequence': 15,
    'summary': 'Product Approval',
    'description': """
Manage product approval.
    """,
    'author': 'Plexada Systems Integrators.',
    'website': 'https://www.plexada-si.com',
    'license': 'LGPL-3',
    'support': 'support@plexada-si.com',
    'depends': ['base_setup', 'product', 'industry_fsm'],
    'installable': True,
    'auto_install': True,
    'application': False,
    'data': [
        'wizards/swap_product_wizard.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
    ],

    'images': ['static/description/banner.png'],
}
