from openerp.tests import common


class TestSaleOrder(common.TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        # create the 10 products for the testing
        # and record the product ids
        ids = []
        for index in range(0, 10):
            name = "testing_product_" + str(index)
            ids.append(self.env['product.product'].create(
                {'name': name}).id
            )
        # # create an empty sale order for testing
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': 1}
        )
        # # create an payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay', 'provider': 'alipay',
                'website_published': True,
                'alipay_pid': 000000,
                'alipay_seller_email': 'luke.zheng@elico-corp.com',
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
        print '---111print---'
        print '-111--0000', self.sale_order.alipay_url_direct_pay
        self.sale_order.state = 'draft'
        self.sale_order._edi_alipay_url_direct_pay()
        print '00----88', self.sale_order.alipay_url_direct_pay
        self.sale_order.state = 'sent'
        self.sale_order._edi_alipay_url_direct_pay()
        print '00--confirmed--88', self.sale_order.alipay_url_direct_pay

    def test_edi_alipay_url_acquirer(self):
        """
            Test alipay url acquirer:
                _get_ids
        """
        # create multi payment acquirer for testing
        self.payment_acquirer = self.env['payment.acquirer'].create(
            {'name': 'alipay', 'provider': 'alipay',
                'website_published': True,
                'alipay_pid': 000000,
                'alipay_seller_email': 'luke.zheng@elico-corp.com',
                'view_template_id': 1,
                'alipay_key': 1,
                'service': 'create_direct_pay_by_user'})
        print '00--2--88', self.sale_order.alipay_url_direct_pay
        self.sale_order._edi_alipay_url_direct_pay()
        print '00--confirmed--88', self.sale_order.alipay_url_direct_pay

        # # null payment acquirer for testing
        self.env['payment.acquirer'].unlink()
        print '00--2--88', self.sale_order.alipay_url_direct_pay
        self.sale_order._edi_alipay_url_direct_pay()

        print '00--confirmed--88', self.sale_order.alipay_url_direct_pay
