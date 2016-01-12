# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Alipay Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Alipay Implementation',
    'version': '8.0.2.0.1',
    'description':
    """
    Alipay Payment Acquirer
    """,
    'author': 'Elico-Corp',
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
        'edi/sale_order_action_data.xml'],
    'installable': True,
}
