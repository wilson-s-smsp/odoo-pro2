# 🎓 Tutorial Odoo Web Library - Step by Step

Tutorial ini akan memandu Anda mempelajari Odoo Web Library secara bertahap menggunakan proyek Asset Management.

## 📚 Daftar Isi

1. [Persiapan](#persiapan)
2. [Basic Components](#basic-components)
3. [Custom Widgets](#custom-widgets)
4. [Dashboard Development](#dashboard-development)
5. [Advanced Features](#advanced-features)
6. [Testing](#testing)

## 1. Persiapan

### Install dan Setup

```bash
# 1. Masuk ke direktori Odoo
cd /path/to/odoo

# 2. Upgrade module
./odoo-bin -u aset_peminjaman -d your_database

# 3. Restart Odoo server
```

### Struktur File yang Akan Dipelajari

```
aset_peminjaman/
├── static/src/
│   ├── js/               # JavaScript components
│   ├── xml/              # QWeb templates  
│   └── css/              # Stylesheets
├── models/               # Python models
└── views/                # XML views
```

## 2. Basic Components

### Step 1: Membuat Component Pertama

Mari mulai dengan component sederhana:

```javascript
// static/src/js/my_first_component.js
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyFirstComponent extends Component {
    setup() {
        this.state = useState({
            message: "Hello Odoo Web Library!"
        });
    }
    
    onClick() {
        this.state.message = "Button clicked!";
    }
}

MyFirstComponent.template = "my_module.MyFirstComponent";

// Register sebagai client action
registry.category("actions").add("my_first_component", MyFirstComponent);
```

### Step 2: Membuat Template

```xml
<!-- static/src/xml/my_templates.xml -->
<templates>
    <t t-name="my_module.MyFirstComponent" owl="1">
        <div class="p-3">
            <h1 t-esc="state.message"/>
            <button class="btn btn-primary" t-on-click="onClick">
                Click Me!
            </button>
        </div>
    </t>
</templates>
```

### Step 3: Register di Manifest

```python
# __manifest__.py
'assets': {
    'web.assets_backend': [
        'my_module/static/src/js/my_first_component.js',
        'my_module/static/src/xml/my_templates.xml',
    ],
},
```

## 3. Custom Widgets

### Step 1: Field Widget Sederhana

```javascript
// static/src/js/my_widget.js
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ColorWidget extends Component {
    get colorStyle() {
        return `background-color: ${this.props.value || '#ffffff'}`;
    }
}

ColorWidget.template = "my_module.ColorWidget";
ColorWidget.props = {
    ...standardFieldProps,
};

// Register sebagai field widget
registry.category("fields").add("color_widget", ColorWidget);
```

### Step 2: Template Widget

```xml
<t t-name="my_module.ColorWidget" owl="1">
    <div class="color-widget d-flex align-items-center">
        <div class="color-preview" t-att-style="colorStyle" 
             style="width: 30px; height: 30px; border: 1px solid #ccc; margin-right: 10px;"/>
        <span t-esc="props.value"/>
    </div>
</t>
```

### Step 3: Menggunakan Widget di View

```xml
<!-- views/my_views.xml -->
<field name="color_field" widget="color_widget"/>
```

## 4. Dashboard Development

### Step 1: Dashboard Component

```javascript
// static/src/js/dashboard.js
/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class Dashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        
        this.state = useState({
            data: {},
            loading: true
        });
        
        onWillStart(async () => {
            await this.loadData();
        });
    }
    
    async loadData() {
        try {
            this.state.loading = true;
            const data = await this.rpc("/web/dataset/call_kw/my.model/get_dashboard_data", {
                model: "my.model",
                method: "get_dashboard_data",
                args: [],
                kwargs: {},
            });
            this.state.data = data;
        } catch (error) {
            this.notification.add("Error loading data", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }
}

Dashboard.template = "my_module.Dashboard";
registry.category("actions").add("my_dashboard", Dashboard);
```

### Step 2: Dashboard Template

```xml
<t t-name="my_module.Dashboard" owl="1">
    <div class="o_action_manager">
        <div class="o_control_panel d-flex">
            <div class="o_cp_left">
                <h2>My Dashboard</h2>
            </div>
            <div class="o_cp_right">
                <button class="btn btn-primary" t-on-click="loadData">
                    <i class="fa fa-refresh"/> Refresh
                </button>
            </div>
        </div>
        
        <div class="o_content p-3">
            <div t-if="state.loading" class="text-center">
                <i class="fa fa-spinner fa-spin fa-2x"/>
                <p>Loading...</p>
            </div>
            
            <div t-else="">
                <div class="row">
                    <div class="col-md-3" t-foreach="state.data.stats" t-as="stat" t-key="stat.key">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 t-esc="stat.value"/>
                                <p t-esc="stat.label"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</t>
```

### Step 3: Backend Method

```python
# models/my_model.py
@api.model
def get_dashboard_data(self):
    """Return dashboard data"""
    return {
        'stats': [
            {'key': 'total', 'label': 'Total Records', 'value': self.search_count([])},
            {'key': 'active', 'label': 'Active', 'value': self.search_count([('active', '=', True)])},
        ]
    }
```

## 5. Advanced Features

### Patch Existing Components

```javascript
import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";

patch(ListController.prototype, "my_module.ListController", {
    setup() {
        this._super();
        console.log("List controller extended!");
    }
});
```

### Service Integration

```javascript
// static/src/js/my_service.js
/** @odoo-module **/

import { registry } from "@web/core/registry";

export const myService = {
    start() {
        return {
            doSomething() {
                console.log("Service method called");
            }
        };
    }
};

registry.category("services").add("my_service", myService);
```

### Using Service

```javascript
import { useService } from "@web/core/utils/hooks";

setup() {
    this.myService = useService("my_service");
}

onClick() {
    this.myService.doSomething();
}
```

## 6. Testing

### Manual Testing

1. **Component Testing**:
   - Buka browser developer tools
   - Check console untuk errors
   - Test interaksi user

2. **Widget Testing**:
   - Buat record baru
   - Test widget di form view
   - Check responsiveness

3. **Dashboard Testing**:
   - Access dashboard menu
   - Test refresh functionality
   - Check data loading

### Debug Tips

```javascript
// Add debug logging
console.log("State:", this.state);
console.log("Props:", this.props);

// Use debugger
debugger;

// Check component in browser
odoo.__DEBUG__.services.action_manager.action_stack
```

## 🎯 Latihan Praktis

### Latihan 1: Simple Counter Component

Buat component yang:
- Memiliki counter yang bisa di-increment/decrement
- Menyimpan state menggunakan `useState`
- Memiliki tombol reset

### Latihan 2: API Integration Widget

Buat widget yang:
- Mengambil data dari API eksternal
- Menampilkan loading state
- Handle error gracefully

### Latihan 3: Custom Kanban Card

Extend kanban view untuk:
- Menambah quick action buttons
- Custom styling
- Drag & drop functionality

## 📝 Checklist Pembelajaran

- [ ] Memahami OWL framework basics
- [ ] Bisa membuat component sederhana
- [ ] Memahami template system
- [ ] Bisa membuat custom field widget
- [ ] Memahami service integration
- [ ] Bisa membuat dashboard
- [ ] Memahami patch system
- [ ] Bisa debug component
- [ ] Memahami lifecycle hooks
- [ ] Bisa handle errors

## 🚀 Next Level

Setelah menguasai dasar-dasar:

1. **Advanced State Management**
2. **Performance Optimization**
3. **Custom View Types**
4. **Mobile Responsiveness**
5. **Real-time Updates**
6. **Testing Framework**

## 💡 Tips Pro

1. **Selalu gunakan `/** @odoo-module **/`**
2. **Import hanya yang diperlukan**
3. **Gunakan TypeScript untuk project besar**
4. **Test di berbagai browser**
5. **Perhatikan performance**
6. **Ikuti convention Odoo**

Happy coding! 🎉 