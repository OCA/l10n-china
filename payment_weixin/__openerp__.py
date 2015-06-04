# -*- coding: utf-8 -*-

{
    'name': 'Tenpay Payment Acquirer',
    'category': 'Website',
    'summary': 'Payment Acquirer: Tenpay Implementation',
    'version': '1.0',
    'description': """Tenpay Payment Acquirer""",
    'author': 'Odoo CN, Jeffery <jeffery9@gmail.com>',
    'depends': ['payment'],
    'data': [
        'views/weixin.xml',
        'views/payment_acquirer.xml',
        'views/res_config_view.xml',
        'data/weixin.xml',
    ],
    'installable': True,
}
