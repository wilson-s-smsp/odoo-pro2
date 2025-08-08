# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    requirement_line_ids = fields.One2many(
        'crm.lead.requirement.line',
        'lead_id',
        string='Qualification Requirements'
    )
    
    @api.model
    def create(self, vals):
        """Override create to auto-generate requirement lines"""
        lead = super(CrmLead, self).create(vals)
        lead._generate_requirement_lines()
        return lead
    
    def _generate_requirement_lines(self):
        """Generate requirement lines based on current stage"""
        for lead in self:
            # Get requirements for current stage or general requirements
            requirements = self.env['qualification.requirement'].search([
                '|',
                ('stage_id', '=', False),  # General requirements
                ('stage_id', '=', lead.stage_id.id if lead.stage_id else False)
            ])
            
            # Create requirement lines that don't exist yet
            existing_req_ids = lead.requirement_line_ids.mapped('requirement_id.id')
            for requirement in requirements:
                if requirement.id not in existing_req_ids:
                    self.env['crm.lead.requirement.line'].create({
                        'lead_id': lead.id,
                        'requirement_id': requirement.id,
                    })
    
    def get_related_opportunities(self):
        """Get other opportunities from the same partner"""
        self.ensure_one()
        if not self.partner_id:
            return self.env['crm.lead']
        
        return self.env['crm.lead'].search([
            ('partner_id', '=', self.partner_id.id),
            ('id', '!=', self.id),
            ('active', '=', True),
            ('type', '=', 'opportunity')
        ])
    
    @api.depends('stage_id')
    def _compute_progress_percentage(self):
        """Compute progress based on stage sequence"""
        for lead in self:
            if lead.stage_id:
                all_stages = self.env['crm.stage'].search([
                    ('team_id', '=', lead.team_id.id if lead.team_id else False)
                ], order='sequence')
                
                if all_stages:
                    current_index = 0
                    for i, stage in enumerate(all_stages):
                        if stage.id == lead.stage_id.id:
                            current_index = i
                            break
                    
                    # Calculate percentage (0-100)
                    if len(all_stages) > 1:
                        progress = (current_index / (len(all_stages) - 1)) * 100
                        lead.progress_percentage = progress
                    else:
                        lead.progress_percentage = 0
                else:
                    lead.progress_percentage = 0
            else:
                lead.progress_percentage = 0
    
    progress_percentage = fields.Float(
        string='Progress Percentage',
        compute='_compute_progress_percentage',
        store=True
    )
    
    def get_qualification_progress(self):
        """Get qualification requirements completion percentage"""
        self.ensure_one()
        if not self.requirement_line_ids:
            return 0
        
        completed = len(self.requirement_line_ids.filtered('is_completed'))
        total = len(self.requirement_line_ids)
        return (completed / total * 100) if total > 0 else 0 