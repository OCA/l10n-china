# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)


# @openerp.tests.common.at_install(False)
# @openerp.tests.common.post_install(True)
class TestSaleOrder(common.TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create({'name': name}).id)
        # # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create({'partner_id': 1})
        # # create an payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay',
             'provider': 'alipay',
             'website_published': True,
             'alipay_pid': 000000,
             'alipay_seller_email': 'dummy',
             'view_template_id': 1,
             'alipay_key': 1,
             'service': 'create_direct_pay_by_user'})
        self.product_ids = self.env['product.product'].search(
            [('id', 'in', ids)])

    def test_edi_alipay_url(self):
        """
            Test alipay url function:
                _get_ids
        """
        _logger.info('---111print---')
        _logger.info('-111--0000' + str(self.sale_order.alipay_url_direct_pay))
        self.sale_order.state = 'draft'
        self.sale_order._edi_alipay_url_direct_pay()
        _logger.info('00----88' + str(self.sale_order.alipay_url_direct_pay))
        self.sale_order.state = 'sent'
        self.sale_order._edi_alipay_url_direct_pay()
        _logger.info(
            '00--confirmed--88' + str(self.sale_order.alipay_url_direct_pay))

    def test_edi_alipay_url_acquirer(self):
        """
            Test alipay url acquirer:
                _get_ids
        """

    def test_edi_alipay_url_direct_pay(self):
        """
            Test _edi_alipay_url_direct_pay:
        """
        # search one record
        self.sale_order._edi_alipay_url_direct_pay()
        # state = sent
        self.sale_order.write({'state': 'sent'})
        # service is create_direct_pay_by_user

        self.payment_acquirer.write({
            'service': 'create_direct_pay_by_user'})
        self.sale_order._edi_alipay_url_direct_pay()
        # service is not create_direct_pay_by_user
        self.payment_acquirer.write({
            'service': 'create_partner_trade_by_buyer'})
        self.sale_order._edi_alipay_url_direct_pay()

        # state = cancel
        self.sale_order.write({'state': 'cancel'})
        self.sale_order._edi_alipay_url_direct_pay()

        # create multi payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay',
             'provider': 'alipay',
             'website_published': True,
             'alipay_pid': 000000,
             'alipay_seller_email': 'dummy',
             'view_template_id': 1,
             'alipay_key': 1,
             'service': 'create_direct_pay_by_user'})
        _logger.info('00--2--88' + str(self.sale_order.alipay_url_direct_pay))
        self.sale_order._edi_alipay_url_direct_pay()
        _logger.info(
            '00--confirmed--88' + str(self.sale_order.alipay_url_direct_pay))

        # # null payment acquirer for testing
        self.env['payment.acquirer'].unlink()
        _logger.info('00--2--88' + str(self.sale_order.alipay_url_direct_pay))
        self.sale_order._edi_alipay_url_direct_pay()

        _logger.info(
            '00--confirmed--88' + str(self.sale_order.alipay_url_direct_pay))
        # state = sent
        self.sale_order.write({'state': 'sent'})
        self.sale_order._edi_alipay_url_direct_pay()
        # state = cancel
        self.sale_order.write({'state': 'cancel'})
        self.sale_order._edi_alipay_url_direct_pay()

        # # null payment acquirer for testing
        self.env['payment.acquirer'].unlink()
        self.sale_order._edi_alipay_url_direct_pay()
