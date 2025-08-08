/** @odoo-module **/

import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";

export class CustomOpportunityView extends Component {
    static template = "smsp_custom_crm.CustomOpportunityTemplate";
    static props = {
        resId: { type: Number, optional: true },
        context: { type: Object, optional: true },
        record: { type: Object, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            opportunity: null,
            relatedOpportunities: [],
            activeTab: 'activities',
            loading: true,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const resId = this.props.resId || this.props.record?.resId;
        if (!resId) return;
        
        try {
            // Load opportunity data
            const opportunity = await this.orm.call(
                "crm.lead",
                "read",
                [resId],
                {
                    fields: [
                        'name', 'partner_id', 'expected_revenue', 'date_deadline',
                        'user_id', 'probability', 'tag_ids', 'stage_id',
                        'requirement_line_ids', 'progress_percentage',
                        'phone', 'email', 'street', 'city', 'country_id'
                    ]
                }
            );

            if (opportunity.length > 0) {
                this.state.opportunity = opportunity[0];
                
                // Load requirement lines
                if (this.state.opportunity.requirement_line_ids.length > 0) {
                    const requirementLines = await this.orm.call(
                        "crm.lead.requirement.line",
                        "read",
                        [this.state.opportunity.requirement_line_ids],
                        {
                            fields: ['requirement_name', 'is_completed', 'notes', 'sequence']
                        }
                    );
                    this.state.opportunity.requirement_lines = requirementLines.sort((a, b) => a.sequence - b.sequence);
                }

                // Load related opportunities
                const relatedOppIds = await this.orm.call(
                    "crm.lead",
                    "get_related_opportunities",
                    [resId]
                );
                
                if (relatedOppIds.length > 0) {
                    this.state.relatedOpportunities = await this.orm.call(
                        "crm.lead",
                        "read",
                        [relatedOppIds],
                        {
                            fields: ['name', 'expected_revenue', 'stage_id', 'probability']
                        }
                    );
                }
            }
        } catch (error) {
            console.error("Error loading opportunity data:", error);
            this.notification.add("Error loading opportunity data", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    async toggleRequirement(requirementLineId) {
        try {
            const requirementLine = this.state.opportunity.requirement_lines.find(
                line => line.id === requirementLineId
            );
            
            if (requirementLine) {
                const newStatus = !requirementLine.is_completed;
                
                await this.orm.call(
                    "crm.lead.requirement.line",
                    "write",
                    [[requirementLineId], { is_completed: newStatus }]
                );
                
                requirementLine.is_completed = newStatus;
                
                this.notification.add(
                    `Requirement ${newStatus ? 'completed' : 'uncompleted'}`,
                    { type: "success" }
                );
            }
        } catch (error) {
            console.error("Error updating requirement:", error);
            this.notification.add("Error updating requirement", { type: "danger" });
        }
    }

    setActiveTab(tab) {
        this.state.activeTab = tab;
    }

    onLogActivity() {
        this.notification.add("Log Activity clicked - Feature coming soon!", { type: "info" });
    }

    onScheduleActivity() {
        this.notification.add("Schedule Activity clicked - Feature coming soon!", { type: "info" });
    }

    getQualificationProgress() {
        if (!this.state.opportunity?.requirement_lines) return 0;
        
        const completed = this.state.opportunity.requirement_lines.filter(line => line.is_completed).length;
        const total = this.state.opportunity.requirement_lines.length;
        
        return total > 0 ? Math.round((completed / total) * 100) : 0;
    }

    formatCurrency(amount) {
        if (!amount) return "Rp 0";
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
        }).format(amount);
    }

    formatDate(dateString) {
        if (!dateString) return "-";
        return new Date(dateString).toLocaleDateString('id-ID');
    }
}

// Patch FormController for custom opportunity view
patch(FormController.prototype, "smsp_custom_crm.FormController", {
    setup() {
        this._super();
        if (this.props.resModel === 'crm.lead') {
            onMounted(() => {
                this.renderCustomOpportunityView();
            });
        }
    },

    renderCustomOpportunityView() {
        const container = this.el?.querySelector('.custom_opportunity_container');
        if (container && this.model.root.resId) {
            // Create and mount custom component
            const customComponent = new CustomOpportunityView(null, {
                resId: this.model.root.resId,
                record: this.model.root,
                context: this.props.context,
            });
            customComponent.mount(container);
        }
    }
});

registry.category("actions").add("smsp_custom_crm.opportunity_view", CustomOpportunityView); 