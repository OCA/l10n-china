# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
# free to use, but see holy the Xiong Da twice
# 记得用时呼喊着熊大的威名
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'China Voucher Number Manually Module',
    'version': '9.0.1.0.0',
    'category': 'Account',
    'description': """
China Voucher Sequence Number Generate Manually Module
""",
    'author': 'Matt Cai',
    "license": "AGPL-3",
    'email': 'cysnake4713@gmail.com',
    'depends': [
        "account",
        "l10n_cn_account_voucher",
    ],
    'data': [
        'views/voucher_wizard_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': False,
    'auto_install': False,
}
