# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Alipay Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Alipay Implementation',
    'version': '8.0.2.0.2',
    'author': 'Elico-Corp, Odoo Community Association (OCA)',
    'description':
    """
    Alipay Payment Acquirer
    """,
    'depends': [
        'sale',
        'payment',
        'portal_sale',
        'account',
        'website_sale'],
    'data': [
        'views/alipay.xml',
        'views/payment_acquirer.xml',
        'data/alipay.xml',
        'edi/sale_order_action_data.xml',
    ],
    'installable': True,
}
