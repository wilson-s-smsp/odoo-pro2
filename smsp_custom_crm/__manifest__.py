# -*- coding: utf-8 -*-
{
    'name': "SMSP Custom CRM",
    'summary': """Custom CRM Opportunity View with OWL Components""",
    'description': """
        Custom CRM module yang menyediakan:
        - Custom tampilan opportunity dengan OWL components
        - Qualification requirements checklist
        - Enhanced opportunity details view
        - Related opportunities tracking
        - Custom progress tracking
    """,
    'author': "Wilson Soeparman",
    'website': "http://www.contohwebsite.com",
    'category': 'Sales/CRM',
    'version': '17.0.1.0.0',
    'depends': ['base', 'crm', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'data/qualification_requirement_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'smsp_custom_crm/static/src/css/opportunity_view.css',
            'smsp_custom_crm/static/src/js/opportunity_view.js',
            'smsp_custom_crm/static/src/xml/opportunity_templates.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 