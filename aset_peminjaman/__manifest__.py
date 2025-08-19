# -*- coding: utf-8 -*-
{
    'name': "Aset Peminjaman Sederhana", # Nama modul yang akan tampil di Odoo
    'summary': """Modul sederhana untuk melacak peminjaman aset kantor.""", # Ringkasan singkat
    'description': """
        Modul ini memungkinkan manajemen aset kantor yang dipinjamkan kepada karyawan.
        Fitur termasuk:
        - Pencatatan aset (nama, nomor seri, status ketersediaan)
        - Pencatatan peminjaman (siapa yang meminjam, kapan, kapan harus kembali, kapan kembali)
        - Update status aset otomatis saat dipinjam/dikembalikan
        - Dashboard interaktif dengan statistik
    """, # Deskripsi detail modul
    'author': "Wilson Soeparman", # Ganti dengan nama Anda
    'website': "http://www.contohwebsite.com", # Opsional, bisa website perusahaan/pribadi

    # Kategori di Odoo App Store (pilih yang sesuai)
    # List kategori: https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    'category': 'Human Resources',
    'version': '0.1', # Versi modul Anda

    # Dependencies: daftar modul Odoo lain yang dibutuhkan modul ini untuk berjalan
    # 'base' selalu wajib karena ini adalah modul inti Odoo
    'depends': ['base', 'mail', 'web'],

    # Data yang akan dimuat saat modul diinstal/di-update
    # Urutan penting: security dulu, baru views, lalu data
    'data': [
        'security/ir.model.access.csv', # Hak akses untuk model kita
        'views/asset_item_views.xml',    # Tampilan untuk model asset.item
        'views/asset_loan_views.xml',    # Tampilan untuk model asset.loan
        'views/menu_items.xml',          # Item menu navigasi (root menu dulu)
        'views/dashboard_views.xml',     # Dashboard views (setelah root menu tersedia)
    ],
    'assets': {
        'web.assets_backend': [
            'aset_peminjaman/static/src/css/asset_dashboard.css',
            'aset_peminjaman/static/src/js/asset_dashboard.js',
            'aset_peminjaman/static/src/xml/asset_templates.xml',
        ],
    },
    # Data demo yang hanya dimuat jika opsi "Load Demo Data" diaktifkan saat instalasi database baru
    'demo': [
        # 'demo/demo_data.xml', # Jika Anda punya data demo, masukkan di sini
    ],
    'installable': True, # Apakah modul ini bisa diinstal? (Hampir selalu True)
    'application': True, # Apakah ini aplikasi utama atau hanya add-on kecil? (True jika aplikasi)
    'auto_install': False, # Apakah otomatis terinstal jika dependensinya terpenuhi? (Jarang True)
    'license': 'LGPL-3', # Lisensi modul Anda (LGPL-3 adalah standar Odoo CE)
}