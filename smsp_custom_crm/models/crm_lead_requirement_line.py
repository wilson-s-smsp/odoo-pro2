# -*- coding: utf-8 -*-
from odoo import models, fields


class CrmLeadRequirementLine(models.Model):
    _name = 'crm.lead.requirement.line'
    _description = 'CRM Lead Requirement Line'
    _order = 'sequence, id'

    lead_id = fields.Many2one(
        'crm.lead',
        string='Opportunity',
        required=True,
        ondelete='cascade'
    )
    
    requirement_id = fields.Many2one(
        'qualification.requirement',
        string='Requirement',
        required=True
    )
    
    is_completed = fields.Boolean(
        string='Completed',
        default=False,
        help='Check if this requirement is completed'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes for this requirement'
    )
    
    sequence = fields.Integer(
        related='requirement_id.sequence',
        store=True,
        readonly=True
    )
    
    # Related fields for easier access
    requirement_name = fields.Char(
        related='requirement_id.name',
        readonly=True
    )
    
    requirement_description = fields.Text(
        related='requirement_id.description',
        readonly=True
    ) 