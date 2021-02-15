# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "bluestar Shipping",
    'description': """
Create Air Frieght and Sea Frieght delivery method
=======================================================

Companies located in Belgium can take advantage of shipping with the
local Post company.

See: 
    """,
    'category': 'Operations/Inventory/Delivery',
    'version': '1.0',
    'application': True,
    'depends': ['delivery', 'mail'],
    'data': [
        'data/delivery_bluestar_data.xml',
#         'views/delivery_bluestar_views.xml', 
        'views/res_config_settings_views.xml',
#         'views/bpost_request_templates.xml',
    ],
    'license': 'OEEL-1',
}
