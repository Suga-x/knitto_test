# -*- coding: utf-8 -*-
{
    'name': "Booking Order",

    'summary': """
        booking_order_AgusRianS_20072024""",

    'description': """
        booking_order_AgusRianS_20072024
    """,

    'author': "Agus Rian S.",
    'website': "-",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','report_py3o'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/service_team_view.xml',
        'views/sale_order_view.xml',
        'views/work_order_view.xml',
        'views/action.xml',
        'report/report_py3o.xml',
    ],

    'installable': True,
    'auto_install': False,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
