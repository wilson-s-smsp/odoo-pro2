/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyLeadComponent extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ name: "", email: "" });

        // Ambil ID record yang sedang dibuka di form
        const leadId = this.props.resId;
        console.log("leadId: ", leadId);

        onMounted(async () => {
            const result = await this.orm.read("crm.lead", [leadId], ["name", "email_from"]);
            console.log("result: ", result);
            if (result.length) {
                this.state.name = result[0].name;
                this.state.email = result[0].email_from;
            }
        });
    }
}
MyLeadComponent.template = "crm_empty.MyLeadComponent";
