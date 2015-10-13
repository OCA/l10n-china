# -*- coding: utf-8 -*-

{
    'name': 'allPay Payment Acquirer',
    'category': 'Website',
    'summary': 'Payment Acquirer: allPay Implementation',
    'version': '1.0',
    'description': """allPay Payment Acquirer""",
    'author': 'Odoo CN Community, Jeffery <jeffery9@gmail.com>',
    'depends': ['payment'],
    'data': [
        'views/allpay.xml',
        'views/payment_acquirer.xml',
        'data/allpay.xml',
    ],
    'installable': True,
    'price': 499.99,
    'currency': 'EUR',
}
