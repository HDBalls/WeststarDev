# -*- coding: utf-8 -*-
{
    'name': "Workshop",

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
    'category': 'Workshop',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'stock', 'product', 'project', 'industry_fsm'],

    # always loaded
    'data': [
        'security/workshop_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/vehicle_model_views.xml',
        'wizards/create_work_order.xml',
        'views/workshop_vehicle_services_view.xml',
        'views/workshop_vehicle_views.xml',
        'views/project_view.xml',
        'views/contact_view.xml',
        'views/view_employee.xml',
        'views/sale_view.xml',
        'reports/workshop_estimate_invoice_header.xml',
        'reports/workshop_estimate_invoice.xml',
        'reports/workshop_account_invoice_2.xml',
        'reports/workshop_account_invoice_3.xml',
        'reports/workshop_account_invoice.xml',
        'reports/workshop_workorder_invoice.xml',
        'workshop_estimate_invoice_header_inherit_cr.xml',
        'reports/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
