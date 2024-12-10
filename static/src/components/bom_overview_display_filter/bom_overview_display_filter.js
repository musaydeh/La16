/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewDisplayFilter } from "@mrp/components/bom_overview_display_filter/bom_overview_display_filter";
import { _t } from "@web/core/l10n/translation";

patch(BomOverviewDisplayFilter.prototype, {
    setup() {
        this._super();
        this.displayOptions = {
            ...this.displayOptions,
            UomUnitPrice: _t("UOM Unit Price"),
        };
    },
});

patch(BomOverviewDisplayFilter, {
    props: {
        ...BomOverviewDisplayFilter.props,
        showOptions: { type: Object },
    },
});
