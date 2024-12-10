from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def cron_compute_price_from_bom(self):
        domain = [("categ_id.auto_compute_price_from_bom", "=", True)]
        products = self.search(domain)
        if products:
            products.action_bom_cost()
