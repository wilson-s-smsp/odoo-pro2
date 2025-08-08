# aset_peminjaman/models/asset_item.py
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AssetItem(models.Model):
    _name = 'asset.item'
    _description = 'Item Aset Kantor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Aset', required=True)
    serial_number = fields.Char(string='Nomor Seri', required=True, copy=False)
    description = fields.Text(string='Deskripsi')
    is_available = fields.Boolean(string='Tersedia', default=True)

    _sql_constraints = [
        (
            'serial_number_unique',
            'unique(serial_number)',
            'Nomor Seri harus unik!',
        ),
    ]
    # --- TAMBAHKAN FIELD BARU INI ---
    manufacturer = fields.Char(string='Pabrikan')
    purchase_date = fields.Date(string='Tanggal Beli')
    warranty_end_date = fields.Date(string='Garansi Berakhir')

    # Relasi One2many ke model peminjaman
    loan_ids = fields.One2many('asset.loan', 'asset_id', string='Riwayat Peminjaman')
    loan_count = fields.Integer(
        string='Jumlah Peminjaman',
        compute='_compute_loan_count'
    )
    image_1920 = fields.Image("Gambar Aset", max_width=1920, max_height=1920)

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for record in self:
            record.loan_count = len(record.loan_ids)

    def action_view_loans(self):
        self.ensure_one()
        return {
            'name': _('Peminjaman Aset'),
            'view_mode': 'tree,form',
            'res_model': 'asset.loan',
            'type': 'ir.actions.act_window',
            'domain': [('asset_id', '=', self.id)],
            'context': {'default_asset_id': self.id},
        }

    # === METODE BARU UNTUK WEB LIBRARY ===
    
    @api.model
    def get_dashboard_data(self):
        """Mengambil data untuk dashboard"""
        # Hitung statistik aset
        total_assets = self.search_count([])
        available_assets = self.search_count([('is_available', '=', True)])
        borrowed_assets = self.search_count([('is_available', '=', False)])
        
        # Hitung statistik peminjaman
        loan_model = self.env['asset.loan']
        total_loans = loan_model.search_count([])
        
        # Peminjaman yang terlambat (belum dikembalikan dan melewati tanggal kembali)
        today = fields.Date.today()
        overdue_loans = loan_model.search_count([
            ('state', '=', 'borrowed'),
            ('return_date', '<', today)
        ])
        
        # Data untuk chart
        chart_data = {
            'available': available_assets,
            'borrowed': borrowed_assets,
            'maintenance': 0,  # Bisa ditambahkan nanti jika ada status maintenance
        }
        
        return {
            'totalAssets': total_assets,
            'availableAssets': available_assets,
            'borrowedAssets': borrowed_assets,
            'totalLoans': total_loans,
            'overdueLoans': overdue_loans,
            'chartData': chart_data,
        }
    
    def toggle_availability(self):
        """Toggle status ketersediaan aset"""
        for record in self:
            # Cek apakah aset sedang dipinjam
            active_loan = self.env['asset.loan'].search([
                ('asset_id', '=', record.id),
                ('state', '=', 'borrowed')
            ], limit=1)
            
            if active_loan and record.is_available:
                raise models.UserError(_(
                    "Aset ini sedang dipinjam dan tidak bisa diubah statusnya."
                ))
            
            record.is_available = not record.is_available
            
            # Log activity
            record.message_post(
                body=_("Status ketersediaan diubah menjadi: %s") % (
                    "Tersedia" if record.is_available else "Tidak Tersedia"
                )
            )
        
        return True
    
    @api.model
    def get_recent_activities(self, limit=10):
        """Mengambil aktivitas terbaru untuk dashboard"""
        recent_loans = self.env['asset.loan'].search([
            ('state', 'in', ['borrowed', 'returned'])
        ], order='create_date desc', limit=limit)
        
        activities = []
        for loan in recent_loans:
            activities.append({
                'id': loan.id,
                'asset_name': loan.asset_id.name,
                'borrower': loan.borrower_name,
                'action': 'dipinjam' if loan.state == 'borrowed' else 'dikembalikan',
                'date': loan.borrow_date if loan.state == 'borrowed' else loan.actual_return_date,
                'state': loan.state,
            })
        
        return activities
