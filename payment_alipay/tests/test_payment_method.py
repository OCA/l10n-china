from openerp.tests import common
import logging
_logger = logging.getLogger(__name__)


class TestPaymentMethod(common.TransactionCase):
    def setUp(self):
        super(TestPaymentMethod, self).setUp()
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
        # self.payment_method = self.env['payment.method'].create(
        #     {})
        self.product_ids = self.env['product.product'].search(
            [('id', 'in', ids)])
