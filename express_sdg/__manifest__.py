# -*- coding: utf-8 -*-
{
    'name': "express_sdg",

    'summary': """
        les express sodigaz""",

    'description': """
        parametrages et plus
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','stock','purchase','point_of_sale','report_xlsx'],

    # always loaded
    'data': [
        'security/express_sdg_security.xml',
        'security/ir.model.access.csv',
        'views/wizards.xml',
        'views/gesparams.xml',       
        'views/etatstemplates.xml',
        'views/etats.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
