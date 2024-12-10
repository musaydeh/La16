from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    update_qty = fields.Float()
    apply_update = fields.Boolean()

    def fill_base_qty(self):
        for line in self.bom_line_ids:
            line.base_qty = line.product_qty

    def update_product_qty_line(self):
        if self.update_qty and self.product_qty:
            balance = self.update_qty / self.product_qty
            int_balance = int(balance)
            for line in self.bom_line_ids:
                line.product_qty = (line.base_qty * int_balance) + (line.base_qty * (balance - int_balance))
                line.bom_id.apply_update = False
                line.bom_id.product_qty = line.bom_id.update_qty

    @api.onchange('apply_update')
    def _onchange_apply_update(self):
        if self.apply_update:
            self.update_qty = 0


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    uom_unit_price = fields.Float(
        string="UOM Unit Price", 
        compute="_compute_subtotal",
        digits='Product Price'
    )
    base_qty = fields.Float()

    @api.depends('product_qty', 'product_id.lst_price')
    def _compute_subtotal(self):
        for line in self:
            line.uom_unit_price = line.product_qty * line.product_id.lst_price
