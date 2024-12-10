# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    auto_compute_price_from_bom = fields.Boolean(string="Auto Compute Price from BoM")
