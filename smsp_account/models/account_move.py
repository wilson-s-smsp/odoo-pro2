# -*- coding: utf-8 -*-

from odoo import models, fields, api


class accountMoveLock(models.Model):
    _inherit = 'account.move'

    has_sale = fields.Boolean(compute="_compute_has_sale",default=False)

    def _compute_has_sale(self):
        for rec in self:
            related_sale_order = self.env['sale.order'].sudo().search([['invoice_ids','=',rec.id]])
            if related_sale_order:
                self.has_sale = True
            else:
                self.has_sale = False
