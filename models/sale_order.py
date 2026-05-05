from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _process_auto_invoice(self, invoice):
        """Keep subscription invoices in draft instead of posting them automatically."""
        return

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)

        # Fix AFIP service period for "mes vencido" plans (l10n_ar field)
        if not hasattr(self.env['account.move'], 'l10n_ar_afip_service_start'):
            return invoices

        for invoice in invoices:
            lines_with_sub = invoice.invoice_line_ids.filtered(
                lambda l: l.sale_line_ids and l.sale_line_ids.order_id.plan_id
            )
            if not lines_with_sub:
                continue
            so = lines_with_sub[0].sale_line_ids.order_id
            if not so.plan_id.bill_end_period:
                continue
            recurring_line = so.order_line.filtered(lambda l: l.recurring_invoice)
            if not recurring_line:
                continue
            new_period_start, new_period_stop, _ratio, _days = recurring_line[0]._get_invoice_line_parameters()
            if new_period_start and new_period_stop:
                billing_period = so.plan_id.billing_period
                invoice.l10n_ar_afip_service_start = new_period_start - billing_period
                invoice.l10n_ar_afip_service_end = new_period_stop - billing_period

        return invoices
