{
    'name': 'Sale Subscription - Keep Invoices in Draft',
    'version': '19.0.1.0.0',
    'category': 'Sales/Subscription',
    'summary': 'Generates subscription invoices in draft state instead of validating them automatically',
    'author': 'Fabrizio',
    'license': 'LGPL-3',
    'depends': [
        'sale_subscription',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
