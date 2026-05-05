from dateutil.relativedelta import relativedelta

from odoo import _, models
from odoo.tools import format_date


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)

        plan = self.order_id.plan_id
        if (
            plan
            and plan.bill_end_period
            and self.recurring_invoice
            and not self._is_delivery()
            and self.order_id.subscription_state != '7_upsell'
        ):
            new_period_start, new_period_stop, _ratio, _days = self._get_invoice_line_parameters()
            if new_period_start and new_period_stop:
                billing_period = plan.billing_period
                past_start = new_period_start - billing_period
                past_stop = new_period_stop - billing_period
                lang_code = self.order_id.partner_id.lang
                format_start = format_date(self.env, past_start, lang_code=lang_code)
                format_stop = format_date(self.env, past_stop, lang_code=lang_code)
                duration = plan.billing_period_display
                period_text = _("%(start)s to %(next)s", start=format_start, next=format_stop)
                # Replace the period line in the description (last \n-separated chunk)
                current_name = res.get('name', '')
                lines = current_name.split('\n')
                if len(lines) > 1:
                    lines[-1] = f"{duration} {period_text}"
                    res['name'] = '\n'.join(lines)

        return res
