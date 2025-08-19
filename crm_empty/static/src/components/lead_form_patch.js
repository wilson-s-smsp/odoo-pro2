/** @odoo-module **/

import { FormRenderer } from "@web/views/form/form_renderer";
import { patch } from "@web/core/utils/patch";
import { mount } from "@odoo/owl";
import { MyLeadComponent } from "./MyLeadComponent";

patch(FormRenderer.prototype, {
    setup() {
        super.setup();
    },
    
    async onMounted() {
        await super.onMounted();
        if (this.props.record.resModel === "crm.lead") {
            const root = this.el.querySelector("#my_lead_root");
            if (root) {
                await mount(MyLeadComponent, root, {
                    props: { resId: this.props.record.resId }
                });
            }
        }
    }
});
