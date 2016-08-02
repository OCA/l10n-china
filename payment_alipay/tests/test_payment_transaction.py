from openerp.tests import common
import logging
_logger = logging.getLogger(__name__)


class TestPaymentTransaction(common.TransactionCase):
    def setUp(self):
        super(TestPaymentTransaction, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create(
                {'name': name}).id
            )
        # create an payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay', 'provider': 'alipay',
                'website_published': True,
                'alipay_pid': 000000,
                'alipay_seller_email': 'luke.zheng@elico-corp.com',
                'view_template_id': 1,
                'alipay_key': 1,
                'service': 'create_direct_pay_by_user'})
        # self.payment_method = self.env['payment.method'].create(
        #     {'name': 'alipay',
        #         'payment_acquirer_id': self.payment_acquirer.id,
        #         'journal_id': 2,
        #         'workflow_process_id': 1})
        # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': 1,
                'name': 'SO-2015-18-0050',
                'payment_method_id': self.payment_method.id,
                'workflow_process_id':
                    self.payment_method.workflow_process_id.id}
        )
        # create an transaction
        self.payment_transaction = self.env['payment.transaction'].create(
            {'reference': 'SO-2015-18-0050',
                'acquirer_id': self.payment_acquirer.id,
                'sale_order_id': self.sale_order.id,
                'amount': 0,
                'currency_id': 1,
                'partner_country_id': 1})
        self.product_ids = self.env['product.product'].search(
            [('id', 'in', ids)])

    def test_alipay_form_get_tx_from_data(self):
        """ Checks if the _alipay_form_get_tx_from_data works properly
        """
        return_data = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015091821001004960062775012',
            'seller_id': u'2088701568026380',
            'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-18-0050',
            'sign': u'0d15f55069ae539ba307ebaa7e299f2d',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-18-0050',
            'payment_type': u'1', 'total_fee': u'0.01',
            'sign_type': u'MD5',
            'notify_time': u'2015-09-18 11:59:52',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoE0j7btVBZMUctZX\
            TD3%2BDtN9jMfdS3RPF1Kt%2F34kTvi9Jk',
            'notify_type': u'trade_status_sync',
            'is_success': u'T', 'buyer_id': u'2088002451351968'}
        self.payment_transaction._alipay_form_get_tx_from_data(return_data)
        pass

    def test_alipay_form_get_invalid_parameters(self):
        """ Checks if the _alipay_form_get_invalid_parameters works properly
        """
        return_data = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015091821001004960062775012',
            'seller_id': u'2088701568026380',
            'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-18-0050',
            'sign': u'0d15f55069ae539ba307ebaa7e299f2d',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-18-0050',
            'payment_type': u'1', 'total_fee': u'0.01',
            'sign_type': u'MD5',
            'notify_time': u'2015-09-18 11:59:52',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoE0j7btVBZMUctZX\
            TD3%2BDtN9jMfdS3RPF1Kt%2F34kTvi9Jk',
            'notify_type': u'trade_status_sync',
            'is_success': u'T', 'buyer_id': u'2088002451351968'}
        self.payment_transaction._alipay_form_get_invalid_parameters(
            self.payment_transaction, return_data)
        pass

    def test_alipay_form_validate(self):
        """ Checks if the _alipay_form_validate works properly
        """
        return_data = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015091821001004960062775012',
            'seller_id': u'2088701568026380',
            'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-18-0050',
            'sign': u'0d15f55069ae539ba307ebaa7e299f2d',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-18-0050',
            'payment_type': u'1', 'total_fee': u'0.01',
            'sign_type': u'MD5',
            'notify_time': u'2015-09-18 11:59:52',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoE0j7btVBZMUctZX\
            TD3%2BDtN9jMfdS3RPF1Kt%2F34kTvi9Jk',
            'notify_type': u'trade_status_sync',
            'is_success': u'T', 'buyer_id': u'2088002451351968'}
        self.payment_transaction._alipay_form_validate(
            self.payment_transaction, return_data)
        pass

    # def test_alipay_auto_payment(self):
    #     """ Checks if the alipay_auto_payment works properly
    #     """
    #     return_data = {
    #         'seller_email': u'sales@elico-corp.com',
    #         'trade_no': u'2015091821001004960062775012',
    #         'seller_id': u'2088701568026380',
    #         'buyer_email': u'cialuo@126.com',
    #         'subject': u'SO-2015-18-0050',
    #         'sign': u'0d15f55069ae539ba307ebaa7e299f2d',
    #         'exterface': u'create_direct_pay_by_user',
    #         'out_trade_no': u'SO-2015-18-0050',
    #         'payment_type': u'1', 'total_fee': u'0.01',
    #         'sign_type': u'MD5',
    #         'notify_time': u'2015-09-18 11:59:52',
    #         'trade_status': u'TRADE_SUCCESS',
    #         'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoE0j7btVBZMUctZX\
    #         TD3%2BDtN9jMfdS3RPF1Kt%2F34kTvi9Jk',
    #         'notify_type': u'trade_status_sync',
    #         'is_success': u'T', 'buyer_id': u'2088002451351968'}
    #     self.payment_transaction.alipay_auto_payment(
    #         self.payment_transaction, return_data)
    #     pass
