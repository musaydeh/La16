/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewComponent } from "@mrp/components/bom_overview/mrp_bom_overview";

patch(BomOverviewComponent.prototype, "boM_ctructure_price_cost", {
    setup() {
        this._super.apply();
        this.state.showOptions.UomUnitPrice = false;
    },

    getReportName(printAll) {
        return this._super.apply(this, arguments) + "&show_uom_unit_price=" + this.state.showOptions.UomUnitPrice;
    }
});
