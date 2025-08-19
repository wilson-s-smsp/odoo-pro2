{
    "name": "CRM Empty",
    "version": "1.0",
    "author": "SMSP",
    "depends": ["crm"],
    "data": [
        "views/crm_lead_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "crm_empty/static/src/components/MyLeadComponent.js",
            "crm_empty/static/src/components/MyLeadComponent.xml",
            "crm_empty/static/src/components/lead_form_patch.js",
        ],
    },

    "installable": True,
    "application": False,
}
