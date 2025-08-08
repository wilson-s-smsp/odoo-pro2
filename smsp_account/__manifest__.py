# -*- coding: utf-8 -*-
{
    'name': "SMSP Account Module Override",

    'summary': """
        App to add minor changes to accounting/invoicing app""",

    'author': "SMSPerkasa",
    'website': "http://www.smsperkasa.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/account_views_extend.xml'
    ],
    'license': 'GPL-3'
}
