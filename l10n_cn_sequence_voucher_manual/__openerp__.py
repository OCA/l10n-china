# -*- coding: utf-8 -*-
# © 2016 <matt.cai>cysnake4713@gmail.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'China Voucher Sequence Number Manual Generation Wizard',
    'summary': 'China Voucher Sequence Number Manual Generation Wizard',
    'version': '9.0.1.0.0',
    'category': 'Account',
    'author': '<matt.cai>cysnake4713@gmail.com, Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'email': 'cysnake4713@gmail.com',
    'application': False,
    'installable': True,
    'depends': [
        'account',
        'l10n_cn_account_voucher',
    ],
    'data': [
        'views/voucher_wizard_view.xml',
    ],
}
