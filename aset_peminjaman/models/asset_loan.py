# aset_peminjaman/models/asset_loan.py
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AssetLoan(models.Model):
    _name = 'asset.loan'
    _description = 'Peminjaman Aset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Referensi Peminjaman',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    asset_id = fields.Many2one(
        'asset.item',
        string='Aset',
        required=True,
        domain=[('is_available', '=', True)],
        help='Pilih aset yang akan dipinjam. '
        'Hanya aset yang tersedia yang akan muncul.',
    )
    description = fields.Text(string='Deskripsi pinjaman')
    borrower_name = fields.Char(string='Peminjam', required=True)
    borrow_date = fields.Date(
        string='Tanggal Pinjam',
        required=True,
        default=lambda self: fields.Date.today(),
    )
    return_date = fields.Date(string='Tanggal Kembali Harapan')
    actual_return_date = fields.Date(string='Tanggal Kembali Aktual')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Dipinjam'),
        ('returned', 'Dikembalikan'),
    ], string='Status', default='draft', readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        print(f"self: {self}")
        print(f"vals: {vals}")
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = (
                self.env['ir.sequence'].next_by_code('asset.loan') or _('New')
            )
        res = super(AssetLoan, self).create(vals)
        return res

    @api.constrains('borrow_date', 'return_date', 'actual_return_date')
    def _check_dates(self):
        for record in self:
            if (
                record.borrow_date
                and record.return_date
                and record.borrow_date > record.return_date
            ):
                raise ValidationError(
                    _("Tanggal Kembali Harapan tidak boleh sebelum Tanggal Pinjam.")
                )
            if (
                record.borrow_date
                and record.actual_return_date
                and record.borrow_date > record.actual_return_date
            ):
                raise ValidationError(
                    _("Tanggal Kembali Aktual tidak boleh sebelum Tanggal Pinjam.")
                )
            if (
                record.return_date
                and record.actual_return_date
                and record.actual_return_date > record.return_date
            ):
                if record.state != 'returned':
                    raise ValidationError(
                        _(
                            "Tanggal Kembali Aktual tidak boleh lebih lama dari Tanggal"
                            "Kembali Harapan."
                        )
                    )

    def action_borrow(self):
        for rec in self:
            if not rec.asset_id:
                raise UserError(_("Pilih aset yang akan dipinjam terlebih dahulu."))
            if not rec.asset_id.is_available:
                raise UserError(_("Aset ini sedang tidak tersedia."))

            rec.state = 'borrowed'
            rec.asset_id.is_available = False
        return True

    def action_return(self):
        for rec in self:
            if rec.state == 'returned':
                raise UserError(_("Peminjaman ini sudah dikembalikan sebelumnya."))

            rec.actual_return_date = fields.Date.today()
            rec.state = 'returned'
            rec.asset_id.is_available = True
        return True

    def action_reset_to_draft(self):
        for rec in self:
            if rec.state == 'borrowed':
                raise UserError(
                    _(
                        "Tidak bisa mereset peminjaman yang sedang aktif. "
                        "Kembalikan aset terlebih dahulu."
                    )
                )
            rec.state = 'draft'
            if rec.asset_id:
                rec.asset_id.is_available = True
            rec.actual_return_date = False
