# -*- coding: utf-8 -*-

from odoo import models
from odoo.tools import float_round


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom = self.env['mrp.bom'].browse(bom_id)
        print(bom, bom_id)
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id)
            print('zzzz', current_line, bom_quantity)
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        if product:
            attachments = self.env['mrp.document'].search(['|', '&', ('res_model', '=', 'product.product'),
                                                           ('res_id', '=', product.id), '&',
                                                           ('res_model', '=', 'product.template'),
                                                           ('res_id', '=', product.product_tmpl_id.id)])
        else:
            product = bom.product_tmpl_id
            attachments = self.env['mrp.document'].search(
                [('res_model', '=', 'product.template'), ('res_id', '=', product.id)])
        operations = self._get_operation_line(product, bom,
                                              float_round(bom_quantity, precision_rounding=1, rounding_method='UP'), 0)
        product_cost = 0.0
        bom_cost = 0.0
        toto_price = 0.0
        company = bom.company_id or self.env.company
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            toto_price += line.product_id.lst_price * line_quantity
            price = line.product_id.uom_id._compute_price(line.product_id.with_company(company).standard_price,
                                                          line.product_uom_id) * line_quantity
            product_cost += price
            if line.child_bom_id:
                factor = line.product_uom_id._compute_quantity(line_quantity,
                                                               line.child_bom_id.product_uom_id) / line.child_bom_id.product_qty
                sub_total = self._get_price(line.child_bom_id, factor, line.product_id)
                print('sub_total 1', sub_total)
            else:
                sub_total = price
                print('sub_total 2', sub_total)
            sub_total = self.env.company.currency_id.round(sub_total)
            print('sub_total 3', sub_total)
            bom_cost += sub_total

        lines = {
            'bom': bom,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'list_price': product.lst_price * bom_quantity,
            'currency': company.currency_id,
            'product': product,
            'code': bom and bom.display_name or '',
            'price': product.uom_id._compute_price(product.with_company(company).standard_price,
                                                   bom.product_uom_id) * bom_quantity,
            'total': sum([op['total'] for op in operations]),
            'level': level or 0,
            'operations': operations,
            'operations_cost': sum([op['total'] for op in operations]),
            'attachments': attachments,
            'toto_price': toto_price,
            'product_cost': product_cost,
            'bom_cost': bom_cost,
            'operations_time': sum([op['duration_expected'] for op in operations])

        }
        components, total = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
        lines['total'] += total
        lines['components'] = components
        byproducts, byproduct_cost_portion = self._get_byproducts_lines(bom, bom_quantity, level, lines['total'])
        lines['byproducts'] = byproducts
        lines['cost_share'] = float_round(1 - byproduct_cost_portion, precision_rounding=0.0001)
        lines['bom_cost'] = lines['total'] * lines['cost_share']
        lines['byproducts_cost'] = sum(byproduct['bom_cost'] for byproduct in byproducts)
        lines['byproducts_total'] = sum(byproduct['product_qty'] for byproduct in byproducts)
        lines['extra_column_count'] = self._get_extra_column_count()
        return lines

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        total = 0
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            company = bom.company_id or self.env.company
            price = line.product_id.uom_id._compute_price(line.product_id.with_company(company).standard_price,
                                                          line.product_uom_id) * line_quantity
            if line.child_bom_id:
                factor = line.product_uom_id._compute_quantity(line_quantity,
                                                               line.child_bom_id.product_uom_id) / line.child_bom_id.product_qty
                sub_total = self._get_price(line.child_bom_id, factor, line.product_id)
            else:
                sub_total = price
            sub_total = self.env.company.currency_id.round(sub_total)
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'list_price': line.product_id.lst_price * line_quantity,
                'code': line.child_bom_id and line.child_bom_id.display_name or '',
                'prod_qty': line_quantity,
                'prod_uom': line.product_uom_id.name,
                'prod_cost': company.currency_id.round(price),
                'parent_id': bom.id,
                'line_id': line.id,
                'level': level or 0,
                'total': sub_total,
                'child_bom': line.child_bom_id.id,
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                'attachments': self.env['mrp.document'].search(['|', '&',
                                                                ('res_model', '=', 'product.product'),
                                                                ('res_id', '=', line.product_id.id), '&',
                                                                ('res_model', '=', 'product.template'),
                                                                ('res_id', '=', line.product_id.product_tmpl_id.id)]),

            })
            total += sub_total
        return components, total
