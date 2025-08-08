/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class AssetDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            totalAssets: 0,
            availableAssets: 0,
            borrowedAssets: 0,
            totalLoans: 0,
            overdueLoans: 0,
            chartData: null,
            loading: false,
        });
        
        this.loadData();
    }

    async loadData() {
        this.state.loading = true;
        try {
            const data = await this.rpc("/web/dataset/call_kw/asset.item/get_dashboard_data", {
                model: "asset.item",
                method: "get_dashboard_data",
                args: [],
                kwargs: {},
            });
            
            Object.assign(this.state, data);
            console.log("Dashboard data loaded:", data);
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            // Fallback to demo data
            Object.assign(this.state, {
                totalAssets: 10,
                availableAssets: 7,
                borrowedAssets: 3,
                totalLoans: 15,
                overdueLoans: 1,
            });
            
            if (this.notification) {
                this.notification.add("Menggunakan data demo. Pastikan model asset.item tersedia.", {
                    type: "warning",
                });
            }
        } finally {
            this.state.loading = false;
        }
    }

    onRefresh() {
        this.loadData();
    }
}

AssetDashboard.template = "aset_peminjaman.AssetDashboard";
AssetDashboard.components = {};

registry.category("actions").add("asset_dashboard", AssetDashboard); 