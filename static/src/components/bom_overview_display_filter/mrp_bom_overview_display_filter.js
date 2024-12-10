/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewDisplayFilter } from "@mrp/components/bom_overview_display_filter/mrp_bom_overview_display_filter";

patch(BomOverviewDisplayFilter.prototype, "boM_ctructure_price_cost", {
    setup() {
        this._super.apply();
        this.displayOptions.UomUnitPrice = this.env._t("UOM Unit Price");
    },
});


patch(BomOverviewDisplayFilter, "boM_ctructure_price_cost", {
    props: {
        ...BomOverviewDisplayFilter.props,
        showOptions: { 
            ...BomOverviewDisplayFilter.showOptions,
            UomUnitPrice: Boolean
        },
    },
});
