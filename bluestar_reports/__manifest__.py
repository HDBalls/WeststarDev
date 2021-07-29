# -*- coding: utf-8 -*-
{
    'name': "bluestar",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product', 'industry_fsm'],

    # always loaded
    'data': [
        'reports/external_layout.xml',
        'reports/report_header.xml',
        'reports/report_proforma.xml',
        'reports/report_proforma_invoice.xml',
        'reports/report_proforma_invoice-JB.xml',
        'reports/account_report.xml',
        'reports/report_proforma_workshop.xml',
        'reports/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
