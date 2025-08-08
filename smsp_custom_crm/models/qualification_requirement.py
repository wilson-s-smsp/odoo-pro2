# -*- coding: utf-8 -*-
from odoo import models, fields


class QualificationRequirement(models.Model):
    _name = 'qualification.requirement'
    _description = 'Master Qualification Requirements'
    _order = 'sequence, name'

    name = fields.Char(
        string='Requirement',
        required=True,
        help='Description of the qualification requirement'
    )
    
    description = fields.Text(
        string='Description',
        help='Detailed description of the requirement'
    )
    
    stage_id = fields.Many2one(
        'crm.stage',
        string='CRM Stage',
        help='Stage where this requirement applies'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of display'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    ) 