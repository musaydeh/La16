/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine, "boM_ctructure_price_cost", {
    props: {
        ...BomOverviewLine.props,
        showOptions: { 
            ...BomOverviewLine.showOptions,
            UomUnitPrice: Boolean
        },
    },
});
