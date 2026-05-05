from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _process_auto_invoice(self, invoice):
        """Keep subscription invoices in draft instead of posting them automatically."""
        return
