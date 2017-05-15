# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

import openerp
from openerp.tests import common

_logger = logging.getLogger(__name__)


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestPaymentAcquirer(common.TransactionCase):
    def setUp(self):
        super(TestPaymentAcquirer, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create({'name': name}).id)
        # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': 1,
             'payment_method_id': 1})

        # create an payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay',
             'provider': 'alipay',
             'website_published': True,
             'alipay_pid': 000000,
             'alipay_seller_email': 'luke.zheng@elico-corp.com',
             'view_template_id': 1,
             'alipay_key': 1,
             'service': 'create_direct_pay_by_user'})

        self.payment_transaction = self.env['payment.transaction'].create(
            {'reference': 'SO-2015-18-0050',
             'acquirer_id': self.payment_acquirer.id,
             'sale_order_id': self.sale_order.id,
             'amount': 0,
             'currency_id': 1,
             'partner_country_id': 1})

        self.product_ids = self.env['product.product'].search(
            [('id', 'in', ids)])

        self.base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')

        self.return_data = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015092421001004960098491428',
            'seller_id': u'2088701568026380',
            'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-24059',
            'sign': u'31ec60b33f2dd89fff2557bfd06cad6f',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-24059',
            'payment_type': u'1',
            'total_fee': u'0.01',
            'sign_type': u'MD5',
            'notify_time': u'2015-09-24 10:55:01',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbTzrlGy8Nc02ac3vWSajR'
                         u'n%2BhdZXlGj0vsq%2FpszXQ5%2B7FyuNo',
            'notify_type': u'trade_status_sync',
            'is_success': u'T',
            'buyer_id': u'2088002451351968'}
        self.payment_transaction = self.env['payment.transaction'].create({
            'reference': u'SO-2015-24059',
            'write_uid': 1,
            'date_create': '2015-09-24 02:54:23',
            'acquirer_id': self.payment_acquirer.id,
            'fees': 0.0,
            'display_name': u'SO-2015-24059',
            'partner_phone': u'1',
            'state': u'draft',
            'alipay_txn_tradeno': False,
            'type': u'form',
            'partner_country_id': 6,
            'sale_order_id': self.sale_order.id,
            'currency_id': 8,
            'amount': 0.01,
            'website_message_ids': []})
