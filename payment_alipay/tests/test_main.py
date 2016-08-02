from openerp.tests import common
import logging
import urllib2

_logger = logging.getLogger(__name__)


class TestPaymentAcquirer(common.TransactionCase):
    def setUp(self):
        super(TestPaymentAcquirer, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create(
                {'name': name}).id
            )
        # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': 1, 'payment_method_id': 1}
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

    def test_alipay_validate_data(self):
        """ Checks if the alipay_validate_data works properly
        """
        post = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015092221001004960062840000',
            'seller_id': u'2088701568026380', 'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-22-067',
            'sign': u'43a9fb7c2aa6a2c6da0429b4a5cdf15a',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-22-067',
            'payment_type': u'1', 'total_fee': u'0.01', 'sign_type': u'MD5',
            'notify_time': u'2015-09-22 14:53:41',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPbBlOjuuIi\
            6ZTD4n7BdzhAUQHo9FESU0zvERPsFx9gyRPS3',
            'notify_type': u'trade_status_sync',
            'is_success': u'T', 'buyer_id': u'2088002451351968'}

        post = {
            'seller_email': u'sales@elico-corp.com',
            'trade_no': u'2015091821001004960062777136',
            'seller_id': u'2088701568026380', 'buyer_email': u'cialuo@126.com',
            'subject': u'SO-2015-18-0050',
            'sign': u'92e16f809e36e17d837d6a019a3fee84',
            'exterface': u'create_direct_pay_by_user',
            'out_trade_no': u'SO-2015-18-0051', 'payment_type': u'1',
            'total_fee': u'0.01', 'sign_type': u'MD5',
            'notify_time': u'2015-09-18 14:40:03',
            'trade_status': u'TRADE_SUCCESS',
            'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoF1yY21Ox%2F%2BWrv8x\
            Lpqp49dm4WewxJJhVVR2acgDvvTmt5',
            'notify_type': u'trade_status_sync',
            'is_success': u'T', 'buyer_id': u'2088002451351968'}
        urllib2.Request(
            self.base_url + '/payment/alipay/notify/')
        # self.alipay_validate_data(post)

    # def test_alipay_autoreceive(self):
    #     """ Checks if the alipay_autoreceive works properly
    #     """

    #     post = {
    #         'seller_email': u'sales@elico-corp.com',
    #         'trade_no': u'2015091821001004960062777136',
    #         'seller_id': u'2088701568026380', 'buyer_email': u'cialuo@126.com',
    #         'subject': u'SO-2015-18-0051',
    #         'sign': u'92e16f809e36e17d837d6a019a3fee84',
    #         'exterface': u'create_direct_pay_by_user',
    #         'out_trade_no': u'SO-2015-18-0051', 'payment_type': u'1',
    #         'total_fee': u'0.01', 'sign_type': u'MD5',
    #         'notify_time': u'2015-09-18 14:40:03',
    #         'trade_status': u'TRADE_SUCCESS',
    #         'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoF1yY21Ox%2F%2BWrv8x\
    #         Lpqp49dm4WewxJJhVVR2acgDvvTmt5',
    #         'notify_type': u'trade_status_sync',
    #         'is_success': u'T', 'buyer_id': u'2088002451351968'}
    #     self.alipay_autoreceive(post)

    # def test_alipay_return(self):
    #     """ Checks if the alipay_return works properly
    #     """
    #     post = {
    #         'seller_email': u'sales@elico-corp.com',
    #         'trade_no': u'2015091821001004960062777136',
    #         'seller_id': u'2088701568026380', 'buyer_email': u'cialuo@126.com',
    #         'subject': u'SO-2015-18-0051',
    #         'sign': u'92e16f809e36e17d837d6a019a3fee84',
    #         'exterface': u'create_direct_pay_by_user',
    #         'out_trade_no': u'SO-2015-18-0051', 'payment_type': u'1',
    #         'total_fee': u'0.01', 'sign_type': u'MD5',
    #         'notify_time': u'2015-09-18 14:40:03',
    #         'trade_status': u'TRADE_SUCCESS',
    #         'notify_id': u'RqPnCoPT3K9%2Fvwbh3InVbPoF1yY21Ox%2F%2BWrv8x\
    #         Lpqp49dm4WewxJJhVVR2acgDvvTmt5',
    #         'notify_type': u'trade_status_sync',
    #         'is_success': u'T', 'buyer_id': u'2088002451351968'}
    #     self.alipay_return(post)
    #     pass

    # def test_find_correct_transcation_alipay(self):
    #     """ Checks if the find_correct_transcation_alipay works properly
    #     """
    #     payment_transaction = self.payment_transaction
    #     self.find_correct_transcation_alipay(payment_transaction)

    # def test_payment_transaction(self):
    #     """ Checks if the payment_transaction works properly
    #     """
    #     acquirer_id = self.payment_acquirer.id
    #     self.payment_transaction(acquirer_id)
    #     pass
