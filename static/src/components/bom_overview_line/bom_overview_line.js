/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/bom_overview_line";

patch(BomOverviewLine, {
    props: {
        ...BomOverviewLine.props,
        showOptions: { type: Object },
    },

    template: "boM_ctructure_price_cost.BomOverviewLine",
});
