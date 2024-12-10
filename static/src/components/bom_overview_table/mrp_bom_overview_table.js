/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewTable } from "@mrp/components/bom_overview_table/mrp_bom_overview_table";

patch(BomOverviewTable.prototype, "boM_ctructure_price_cost", {
    //---- Getters ----

    get showUomUnitPrice() {
        return this.props.showOptions.UomUnitPrice;
    }
});

patch(BomOverviewTable, "boM_ctructure_price_cost", {
    props: {
        ...BomOverviewTable.props,
        showOptions: { 
            ...BomOverviewTable.showOptions,
            UomUnitPrice: Boolean
        },
    },
});
