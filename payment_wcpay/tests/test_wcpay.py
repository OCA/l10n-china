# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

import openerp
from openerp.tests import common

_logger = logging.getLogger(__name__)


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class AcquirerWcpayTestCase(common.TransactionCase):
    def setUp(self):
        super(AcquirerWcpayTestCase, self).setUp()
        self.pay_model = self.env['payment.acquirer']
        self.partner = self.env['res.partner']
        self.country = self.env['res.country']
        self.currency = self.env['res.currency']

    def test_wcpay_form_generate_values(self):
        country = self.country.browse(3)
        state = False

        partner_values = {
            'lang': u'en_US',
            'city': u'cc',
            'first_name': u'Administrator',
            'last_name': '',
            'name': u'Administrator',
            'zip': u'cc',
            'country': country,
            'country_id': 3,
            'phone': u'cc',
            'state': state,
            'address': u'cc cc',
            'email': u'admin@example.com'
        }
        tx_values = {
            'amount': 1.0,
            'reference': u'SO0001000',
        }

        partner_values_result, wcpay_tx_values_result = \
            self.pay_model.wcpay_form_generate_values(
                partner_values, tx_values
            )

        payment_type = False
        if wcpay_tx_values_result['payment_type']:
            payment_type = True

        notify_url = False
        if wcpay_tx_values_result['notify_url']:
            notify_url = True

        self.assertTrue(payment_type)
        self.assertTrue(notify_url)
        self.assertEquals(wcpay_tx_values_result['total_fee'], 1.0)
        self.assertEquals(wcpay_tx_values_result['out_trade_no'], u'SO0001000')
        self.assertEquals(wcpay_tx_values_result['price'], 1.0)
        self.assertEquals(wcpay_tx_values_result['subject'], u'SO0001000')
        self.assertEquals(wcpay_tx_values_result['quantity'], 1)
        self.assertEquals(wcpay_tx_values_result['sign_type'], 'MD5')

    def test_wcpay_get_wcpay_urls(self):
        url = self.pay_model._get_wcpay_urls('test')

        if url:
            self.assertTrue(url)
        else:
            self.assertFalse(url)

    def test_get_providers(self):
        providers = self.pay_model._get_providers()

        count = providers.count(['wcpay', 'Wechat Pay'])
        self.assertEquals(count, 1)
