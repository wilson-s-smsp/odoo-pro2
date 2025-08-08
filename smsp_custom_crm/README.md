# SMSP Custom CRM

Custom CRM module untuk Odoo 17 yang menyediakan tampilan opportunity yang disesuaikan dengan kebutuhan bisnis.

## Fitur

### 1. Custom Opportunity View
- Tampilan opportunity yang dipersonalisasi dengan layout full-width
- Progress bar berdasarkan stage CRM
- Interface yang user-friendly dengan OWL components

### 2. Qualification Requirements
- Master data requirements yang dapat dikonfigurasi
- Checklist requirements per opportunity
- Progress tracking berdasarkan completion percentage
- Automatic generation saat opportunity dibuat

### 3. Enhanced Customer Information
- Informasi customer yang lengkap dari res.partner
- Key contacts display
- Related opportunities tracking

### 4. Next Actions & Activities
- Static next actions (scalable untuk integrasi activity)
- Tombol Log Activity dan Schedule Activity (UI only)
- Tabs untuk Activities, Documents, dan Notes

## Models

### qualification.requirement
Master data untuk menyimpan template qualification requirements.

**Fields:**
- `name` (Char): Nama requirement
- `description` (Text): Deskripsi detail
- `stage_id` (Many2one): Stage CRM terkait
- `sequence` (Integer): Urutan tampilan
- `active` (Boolean): Status aktif

### crm.lead.requirement.line
Model perantara untuk menghubungkan opportunity dengan requirements.

**Fields:**
- `lead_id` (Many2one): Referensi ke crm.lead
- `requirement_id` (Many2one): Referensi ke qualification.requirement
- `is_completed` (Boolean): Status completion
- `notes` (Text): Catatan tambahan
- `sequence` (Integer): Urutan tampilan

### crm.lead (Extended)
Extend model crm.lead dengan field dan method tambahan.

**New Fields:**
- `requirement_line_ids` (One2many): Daftar requirement lines
- `progress_percentage` (Float): Persentase progress berdasarkan stage

**New Methods:**
- `get_related_opportunities()`: Mendapatkan opportunity lain dari customer sama
- `get_qualification_progress()`: Menghitung progress completion requirements
- `_generate_requirement_lines()`: Auto-generate requirement lines

## Instalasi

1. Copy folder `smsp_custom_crm` ke direktori addons Odoo
2. Update Apps list di Odoo
3. Install module "SMSP Custom CRM"
4. Module akan otomatis menggantikan form view opportunity standar

## Konfigurasi

### Qualification Requirements
1. Buka Apps > SMSP Custom CRM
2. Konfigurasi master qualification requirements sesuai kebutuhan
3. Set stage_id jika requirement berlaku untuk stage tertentu
4. Atur sequence untuk urutan tampilan

### Data Demo
Module sudah include sample qualification requirements yang umum digunakan dalam sales process.

## Technical Details

### OWL Components
- `CustomOpportunityView`: Main component untuk tampilan opportunity
- `CustomOpportunityFormController`: Form controller yang terintegrasi

### Assets
- CSS: `static/src/css/opportunity_view.css`
- JS: `static/src/js/opportunity_view.js`
- XML Templates: `static/src/xml/opportunity_templates.xml`

### Dependencies
- base
- crm
- mail
- web

## Customization

Module ini dirancang untuk mudah dikustomisasi:

1. **Warna dan Styling**: Edit file CSS untuk mengubah appearance
2. **Requirements**: Tambah/edit master requirements via UI atau data XML
3. **Fields**: Extend models untuk menambah field sesuai kebutuhan
4. **Logic**: Modify JavaScript untuk menambah interactivity

## Roadmap

- [ ] Integrasi dengan activity module
- [ ] Advanced reporting dan analytics
- [ ] Mobile responsive design
- [ ] Email template integration
- [ ] Document management integration

## Support

Untuk support dan customization, hubungi tim development. 