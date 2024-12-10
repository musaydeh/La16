/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverview } from "@mrp/components/bom_overview/bom_overview";
import { useState } from "@odoo/owl";

patch(BomOverview.prototype, {
    setup() {
        this._super();
        this.state = useState({
            ...this.state,
            showOptions: {
                ...this.state.showOptions,
                UomUnitPrice: false,
            },
        });
    },

    getReportParams() {
        const params = this._super();
        return {
            ...params,
            show_uom_unit_price: this.state.showOptions.UomUnitPrice,
        };
    },
});
