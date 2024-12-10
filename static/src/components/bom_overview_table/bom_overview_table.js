/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewTable } from "@mrp/components/bom_overview_table/bom_overview_table";

patch(BomOverviewTable.prototype, {
    get showUomUnitPrice() {
        return this.props.showOptions.UomUnitPrice;
    },
});

patch(BomOverviewTable, {
    props: {
        ...BomOverviewTable.props,
        showOptions: { type: Object },
    },

    template: "boM_ctructure_price_cost.BomOverviewTable",
});
