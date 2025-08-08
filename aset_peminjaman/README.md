# Aset Peminjaman - Learning Odoo Web Library

Proyek ini adalah contoh implementasi Odoo Web Library untuk sistem manajemen aset peminjaman. Modul ini mendemonstrasikan berbagai komponen dan fitur yang tersedia dalam Odoo Web Library.

## 🚀 Fitur Web Library yang Diimplementasikan

### 1. Dashboard Interaktif (`asset_dashboard.js`)
- **Component**: `AssetDashboard`
- **Template**: `aset_peminjaman.AssetDashboard`
- **Fitur**:
  - Cards statistik real-time
  - Chart.js integration untuk visualisasi data
  - Refresh button dengan RPC calls
  - Responsive layout

### 2. Custom Form Widgets (`asset_form_widget.js`)
- **AssetStatusWidget**: Widget khusus untuk menampilkan status aset dengan icon dan warna
- **LoanCountWidget**: Badge widget untuk menampilkan jumlah peminjaman
- **Props**: Menggunakan `standardFieldProps` untuk kompatibilitas

### 3. Enhanced Kanban Records (`asset_kanban_record.js`)
- **Patch System**: Menggunakan `patch()` untuk extend `KanbanRecord`
- **Quick Actions**: Tombol untuk toggle availability langsung dari kanban
- **Notifications**: Service notification untuk feedback user
- **RPC Integration**: Pemanggilan method backend

### 4. Chart Components (`asset_chart.js`)
- **Chart.js Integration**: Loading external library dengan `loadJS`
- **Dynamic Data**: Props-based data binding
- **Lifecycle Management**: Proper cleanup dengan `willUnmount`
- **Responsive Design**: Auto-resize charts

### 5. QWeb Templates (`asset_templates.xml`)
- **Owl Framework**: Template dengan `owl="1"`
- **Template Composition**: Nested components
- **Event Handling**: `t-on-click` untuk interaksi
- **Dynamic Classes**: `t-attf-class` untuk styling kondisional

## 📁 Struktur File

```
aset_peminjaman/
├── static/src/
│   ├── js/
│   │   ├── asset_dashboard.js      # Dashboard component
│   │   ├── asset_form_widget.js    # Custom form widgets
│   │   ├── asset_kanban_record.js  # Kanban enhancements
│   │   ├── asset_chart.js          # Chart components
│   │   └── main.js                 # Main entry point
│   ├── xml/
│   │   └── asset_templates.xml     # QWeb templates
│   └── css/
│       └── asset_dashboard.css     # Custom styles
├── models/
│   └── asset_item.py              # Extended with web methods
└── views/
    └── dashboard_views.xml        # Client actions & views
```

## 🎯 Konsep Web Library yang Dipelajari

### 1. OWL Framework (Odoo Web Library)
```javascript
import { Component, useState } from "@odoo/owl";

export class MyComponent extends Component {
    setup() {
        this.state = useState({ data: null });
    }
}
```

### 2. Service Integration
```javascript
import { useService } from "@web/core/utils/hooks";

setup() {
    this.rpc = useService("rpc");
    this.notification = useService("notification");
}
```

### 3. Registry System
```javascript
import { registry } from "@web/core/registry";

// Register field widget
registry.category("fields").add("my_widget", MyWidget);

// Register client action
registry.category("actions").add("my_action", MyAction);
```

### 4. Patch System
```javascript
import { patch } from "@web/core/utils/patch";

patch(ExistingComponent.prototype, "my_module.Extension", {
    newMethod() {
        // Your extension code
    }
});
```

### 5. Template System
```xml
<t t-name="my_module.MyTemplate" owl="1">
    <div t-on-click="onClick" t-attf-class="{{dynamicClass}}">
        <t t-esc="state.data"/>
    </div>
</t>
```

## 🔧 Cara Menggunakan

### 1. Install Module
```bash
# Upgrade module
./odoo-bin -u aset_peminjaman -d your_database
```

### 2. Akses Dashboard
- Menu: Asset Management > Dashboard
- URL: `/web#action=asset_dashboard`

### 3. Test Custom Widgets
- Buka Asset Item form
- Lihat widget status dan loan count badge
- Test toggle availability di kanban view

### 4. Customize Components
```javascript
// Extend dashboard
export class MyDashboard extends AssetDashboard {
    setup() {
        super.setup();
        // Your customizations
    }
}
```

## 📚 Learning Resources

### Backend Integration
```python
@api.model
def get_dashboard_data(self):
    """Method yang dipanggil dari frontend"""
    return {
        'totalAssets': self.search_count([]),
        'chartData': {...}
    }
```

### RPC Calls
```javascript
const data = await this.rpc("/web/dataset/call_kw/asset.item/get_dashboard_data", {
    model: "asset.item",
    method: "get_dashboard_data",
    args: [],
    kwargs: {},
});
```

### Widget Development
```javascript
export class MyWidget extends Component {
    get computedValue() {
        return this.props.value + " (processed)";
    }
}

MyWidget.template = "my_module.MyWidget";
MyWidget.props = { ...standardFieldProps };
```

## 🎨 Styling dan CSS

### Custom CSS Classes
- `.asset-dashboard`: Main dashboard container
- `.stats-card`: Animated statistic cards
- `.asset-status-widget`: Status indicator widget
- `.loan-count-badge`: Colored badge for counts

### Bootstrap Integration
- Menggunakan Bootstrap classes: `card`, `badge`, `btn`
- Responsive grid: `col-lg-*`, `col-md-*`
- Flexbox utilities: `d-flex`, `justify-content-between`

## 🔍 Advanced Features

### 1. Dynamic Loading
```javascript
await loadJS("https://cdn.jsdelivr.net/npm/chart.js");
```

### 2. Lifecycle Management
```javascript
setup() {
    onMounted(() => this.initChart());
}

willUnmount() {
    if (this.chart) this.chart.destroy();
}
```

### 3. State Management
```javascript
this.state = useState({
    loading: false,
    data: null,
    error: null
});
```

### 4. Error Handling
```javascript
try {
    const result = await this.rpc(...);
} catch (error) {
    this.notification.add("Error: " + error.message, {
        type: "danger"
    });
}
```

## 🚦 Best Practices

1. **Always use `/** @odoo-module **/`** at the top of JS files
2. **Import only what you need** to optimize loading
3. **Use `useService()` hook** for accessing Odoo services
4. **Handle errors gracefully** with try-catch blocks
5. **Clean up resources** in `willUnmount()`
6. **Use semantic CSS classes** for maintainability
7. **Test widgets in different views** (form, tree, kanban)

## 🎓 Next Steps

1. **Extend Dashboard**: Add more charts and statistics
2. **Create Custom Views**: Build completely new view types
3. **Add Animations**: Implement loading states and transitions
4. **Mobile Optimization**: Enhance responsive design
5. **Performance Optimization**: Implement data caching
6. **Advanced Widgets**: Create field-specific widgets
7. **Integration**: Connect with external APIs or services

## 📞 Support

Untuk pertanyaan atau masalah:
- Dokumentasi Odoo: https://www.odoo.com/documentation/
- OWL Framework: https://github.com/odoo/owl
- Community: https://www.odoo.com/forum/ 