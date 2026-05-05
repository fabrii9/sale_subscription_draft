from odoo import fields, models


class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'

    bill_end_period = fields.Boolean(
        string="Facturar Mes Vencido",
        default=False,
        help="Si está activado, el período de servicio en la factura mostrará "
             "el mes anterior al período de facturación (comportamiento de 'mes vencido'). "
             "Aplica al Período Facturado (AFIP) y a la descripción de cada línea.",
    )
