# -*- coding: utf-8 -*-

from odoo import models


class ReportBomStructure(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    def _get_pdf_doc(self, bom_id, data, quantity, product_variant_id=None):
        doc = super()._get_pdf_doc(bom_id, data, quantity, product_variant_id)
        doc["show_uom_unit_price"] = True if data and data.get("show_uom_unit_price") == "true" else False

        return doc

    def _get_bom_data(self, bom, warehouse, product=False, line_qty=False, bom_line=False, level=0, parent_bom=False,
                      index=0, product_info=False, ignore_stock=False):
        res = super()._get_bom_data(bom, warehouse, product, line_qty, bom_line, level, parent_bom, index, product_info,
                                    ignore_stock)

        uom_unit_price = 0
        if bom_line:
            uom_unit_price = bom_line.uom_unit_price

        res["uom_unit_price"] = uom_unit_price

        return res

    def _get_component_data(self, bom, warehouse, bom_line, line_quantity, level, index, product_info,
                            ignore_stock=False):
        res = super()._get_component_data(bom, warehouse, bom_line, line_quantity, level, index, product_info,
                                          ignore_stock)

        uom_unit_price = 0
        if bom_line:
            uom_unit_price = bom_line.uom_unit_price

        res["uom_unit_price"] = uom_unit_price
        return res

    def add_uom_unit_price_bom_array_lines(self, lines_components, components, index):
        for component in components:
            lines_components[index]["uom_unit_price"] = component["uom_unit_price"]
            index += 1

            if component.get('components', []):
                index = self.add_uom_unit_price_bom_array_lines(lines_components, component.get('components', []),
                                                                index)

        return index

    def _get_bom_array_lines(self, data, level, unfolded_ids, unfolded, parent_unfolded):
        lines = super()._get_bom_array_lines(data, level, unfolded_ids, unfolded, parent_unfolded)
        lines_components = []
        for line in lines:
            if "bom_id" in line.keys():
                lines_components.append(line)

        self.add_uom_unit_price_bom_array_lines(lines_components, data.get('components', []), 0)

        return lines
