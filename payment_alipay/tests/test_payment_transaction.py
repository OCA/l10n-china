# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

import openerp
from openerp.tests import common

_logger = logging.getLogger(__name__)


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestPaymentTransaction(common.TransactionCase):
    def setUp(self):
        super(TestPaymentTransaction, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create({'name': name}).id)
        # create an payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {
                'name': 'alipay',
                'provider': 'alipay',
                'website_published': True,
                'alipay_pid': 000000,
                'alipay_seller_email': 'dummy',
                'view_template_id': 1,
                'alipay_key': 1,
                'service': 'create_direct_pay_by_user'
            }
        )
        # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create(
            {
                'partner_id': 1,
                'name': 'SAJ2016080303410037'
            }
        )
        self.account_invoice = self.env['account.invoice'].create(
            {
                'account_id': 1,
                'partner_id': 1,
                'number': 'SAJ2016080303410037'
            }
        )
        # create an transaction
        self.payment_transaction = self.env['payment.transaction'].create(
            {
                'reference': 'SAJ2016080303410037',
                'acquirer_id': self.payment_acquirer.id,
                'sale_order_id': self.sale_order.id,
                'account_invoice_id': self.account_invoice.id,
                'amount': 0,
                'currency_id': 1,
                'partner_country_id': 1
            }
        )
        self.product_ids = self.env['product.product'].search(
            [('id', 'in', ids)])

    def test_alipay_form_get_tx_from_data(self):
        """
        Checks if the _alipay_form_get_tx_from_data works properly
        """
        return_data = {
            'buyer_email': u'234082230@qq.com',
            'buyer_id': u'2088002032609743',
            'discount': u'0.00',
            'gmt_create': u'2016-08-03 11:42:03',
            'gmt_payment': u'2016-08-03 11:42:25',
            'is_total_fee_adjust': u'N',
            'notify_id': u'4cfcf56af12f37b0943c7a1105aea55lpm',
            'notify_time': u'2016-08-03 11:42:25',
            'notify_type': u'trade_status_sync',
            'out_trade_no': u'SAJ2016080303410037',
            'payment_type': u'1',
            'price': u'0.01',
            'quantity': u'1',
            'seller_email': u'sales@elico-corp.com',
            'seller_id': u'2088701568026380',
            'sign': u'89b8cad3e39427f02afd30a8e2b588de',
            'sign_type': u'MD5',
            'subject': u'SAJ2016080303410037',
            'total_fee': u'0.01',
            'trade_no': u'2016080321001004740210408910',
            'trade_status': u'TRADE_SUCCESS',
            'use_coupon': u'N'
        }
        self.payment_transaction._alipay_form_get_tx_from_data(return_data)

    def test_alipay_form_get_invalid_parameters(self):
        """
        Checks if the _alipay_form_get_invalid_parameters works properly
        """
        return_data = {
            'buyer_email': u'234082230@qq.com',
            'buyer_id': u'2088002032609743',
            'discount': u'0.00',
            'gmt_create': u'2016-08-03 11:42:03',
            'gmt_payment': u'2016-08-03 11:42:25',
            'is_total_fee_adjust': u'N',
            'notify_id': u'4cfcf56af12f37b0943c7a1105aea55lpm',
            'notify_time': u'2016-08-03 11:42:25',
            'notify_type': u'trade_status_sync',
            'out_trade_no': u'SAJ2016080303410037',
            'payment_type': u'1',
            'price': u'0.01',
            'quantity': u'1',
            'seller_email': u'sales@elico-corp.com',
            'seller_id': u'2088701568026380',
            'sign': u'89b8cad3e39427f02afd30a8e2b588de',
            'sign_type': u'MD5',
            'subject': u'SAJ2016080303410037',
            'total_fee': u'0.01',
            'trade_no': u'2016080321001004740210408910',
            'trade_status': u'TRADE_SUCCESS',
            'use_coupon': u'N'
        }
        self.payment_transaction._alipay_form_get_invalid_parameters(
            self.payment_transaction, return_data)

    def test_alipay_form_validate(self):
        """ Checks if the _alipay_form_validate works properly
        """
        return_data = {
            'buyer_email': u'234082230@qq.com',
            'buyer_id': u'2088002032609743',
            'discount': u'0.00',
            'gmt_create': u'2016-08-03 11:42:03',
            'gmt_payment': u'2016-08-03 11:42:25',
            'is_total_fee_adjust': u'N',
            'notify_id': u'4cfcf56af12f37b0943c7a1105aea55lpm',
            'notify_time': u'2016-08-03 11:42:25',
            'notify_type': u'trade_status_sync',
            'out_trade_no': u'SAJ2016080303410037',
            'payment_type': u'1',
            'price': u'0.01',
            'quantity': u'1',
            'seller_email': u'sales@elico-corp.com',
            'seller_id': u'2088701568026380',
            'sign': u'89b8cad3e39427f02afd30a8e2b588de',
            'sign_type': u'MD5',
            'subject': u'SAJ2016080303410037',
            'total_fee': u'0.01',
            'trade_no': u'2016080321001004740210408910',
            'trade_status': u'TRADE_SUCCESS',
            'use_coupon': u'N'
        }
        self.payment_transaction._alipay_form_validate(
            self.payment_transaction, return_data)
