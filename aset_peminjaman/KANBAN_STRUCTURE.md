# 📋 Struktur DOM Kanban di Odoo

## 🏗️ Struktur DOM yang Dihasilkan

Ketika kita membuat kanban view di Odoo, framework akan otomatis membungkus template kita dengan element tambahan:

### Struktur Aktual di Browser:
```html
<div class="o_kanban_view">
    <div class="o_kanban_renderer">
        <!-- Auto-generated wrapper oleh Odoo -->
        <div role="article" 
             class="o_kanban_record d-flex flex-grow-1 flex-md-shrink-1 flex-shrink-0" 
             data-id="datapoint_6" 
             tabindex="0">
            
            <!-- Template kita mulai dari sini -->
            <div class="oe_kanban_card oe_kanban_global_click asset_kanban_card">
                <div class="asset_kanban_image">
                    <img class="asset_image" src="..."/>
                    <div class="asset_status_badge">
                        <span class="badge badge-success">✓ Tersedia</span>
                    </div>
                </div>
                <div class="oe_kanban_details asset_kanban_content">
                    <!-- Konten kita -->
                </div>
            </div>
        </div>
    </div>
</div>
```

### Template yang Kita Tulis:
```xml
<t t-name="kanban-box">
    <div class="oe_kanban_card oe_kanban_global_click asset_kanban_card">
        <!-- Konten kita -->
    </div>
</t>
```

## 🎯 Element yang Auto-Generated

### 1. **Wrapper Record**
```html
<div role="article" 
     class="o_kanban_record d-flex flex-grow-1 flex-md-shrink-1 flex-shrink-0" 
     data-id="datapoint_6" 
     tabindex="0">
```

**Fungsi:**
- Container untuk setiap record kanban
- Menangani accessibility (role="article", tabindex)
- Menyediakan data-id untuk identifikasi record
- Mengatur flexbox layout

### 2. **Classes yang Ditambahkan Odoo:**
- `o_kanban_record`: Identifier utama
- `d-flex`: Display flex
- `flex-grow-1`: Flex grow
- `flex-md-shrink-1`: Responsive flex shrink
- `flex-shrink-0`: Flex shrink behavior

## 🎨 Cara Styling yang Benar

### ❌ Yang Tidak Bisa Kita Kontrol:
```css
/* Ini tidak akan berfungsi karena element dibuat otomatis */
.o_kanban_record {
    /* Styling kita akan di-override */
}
```

### ✅ Cara yang Benar:
```css
/* Reset wrapper untuk menghindari konflik */
.o_kanban_record {
    margin: 8px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Style card kita */
.asset_kanban_card {
    width: 100%;
    /* styling kita */
}

/* Hover effect melalui wrapper */
.o_kanban_record:hover .asset_kanban_card {
    transform: translateY(-4px);
}
```

## 🔧 Best Practices

### 1. **Jangan Fight Framework**
- Terima bahwa Odoo akan membuat wrapper
- Style around the wrapper, bukan melawan nya

### 2. **Use !important Sparingly**
- Hanya untuk reset wrapper styles
- Jangan gunakan untuk styling utama

### 3. **Responsive Design**
- Framework wrapper sudah responsive
- Fokus pada konten di dalam card

### 4. **Accessibility**
- Wrapper sudah handle accessibility
- Jangan hapus role dan tabindex

## 🐛 Common Issues

### 1. **Double Margins**
```css
/* Problem: margin ganda */
.o_kanban_record { margin: 10px; }
.asset_kanban_card { margin: 10px; }

/* Solution: margin hanya di wrapper */
.o_kanban_record { margin: 8px !important; }
.asset_kanban_card { margin: 0; }
```

### 2. **Hover Effects Not Working**
```css
/* Problem: hover di card tidak bekerja */
.asset_kanban_card:hover { transform: scale(1.05); }

/* Solution: hover di wrapper */
.o_kanban_record:hover .asset_kanban_card { transform: scale(1.05); }
```

### 3. **Flexbox Conflicts**
```css
/* Problem: flexbox dari wrapper mengganggu layout */
.asset_kanban_card { display: block; } /* Tidak efektif */

/* Solution: bekerja dengan flexbox */
.asset_kanban_card { 
    width: 100%; 
    display: flex;
    flex-direction: column;
}
```

## 📱 Responsive Behavior

Framework wrapper menggunakan Bootstrap classes:
- `flex-md-shrink-1`: Shrink pada medium screens
- `flex-shrink-0`: Tidak shrink pada small screens

Kita harus menyesuaikan styling kita:
```css
@media (max-width: 768px) {
    .o_kanban_record {
        margin: 4px !important;
    }
    
    .asset_kanban_card {
        max-width: 100%;
    }
}
```

## 💡 Tips

1. **Inspect Element** untuk melihat struktur sebenarnya
2. **Test di berbagai screen sizes**
3. **Gunakan browser dev tools** untuk debug CSS
4. **Jangan lawan framework**, bekerja sama dengannya

---

**Note:** Struktur ini adalah behavior standard Odoo dan tidak bisa diubah tanpa customization core framework. 