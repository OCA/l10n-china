# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import pprint
import urlparse

from openerp.addons.report.controllers.main import ReportController
from openerp.addons.web.http import route
from openerp.addons.website_sale.controllers.main import website_sale

from openerp import http, SUPERUSER_ID
from ..models import weixinsdk
from ..models.weixinsdk import Wxpay_server_pub
from openerp.http import request

_logger = logging.getLogger(__name__)


class weixin(object):
    def set_wcpayconf(self, acquirer):
        wxpayconf = weixinsdk.WxPayConf_pub
        wxpayconf.APPID = acquirer.appid
        wxpayconf.APPSECRET = acquirer.appsecret
        wxpayconf.MCHID = acquirer.mchid
        wxpayconf.KEY = acquirer.key
        wxpayconf.SSLCERT_PATH = acquirer.sslcert_path
        wxpayconf.SSLKEY_PATH = acquirer.sslkey_path
        wxpayconf.CURL_TIMEOUT = acquirer.curl_timeout
        wxpayconf.HTTP_CLIENT = acquirer.http_client
        wxpayconf.SPBILL_CREATE_IP = acquirer.ip_address
        return wxpayconf

    def connect_wcpay(self, cr, uid, tx):
        base_url = request.registry.get('ir.config_parameter').get_param(
            cr, uid, 'web.base.url')
        notify_url = '%s' % urlparse.urljoin(
            base_url, WcpayController._notify_url)
        unifiedorder = weixinsdk.UnifiedOrder_pub()
        unifiedorder.setParameter('out_trade_no', tx.reference)
        unifiedorder.setParameter('body', tx.reference)
        unifiedorder.setParameter(
            'total_fee', '%s' % int(tx.amount * 100))
        unifiedorder.setParameter('notify_url', notify_url)
        unifiedorder.setParameter('trade_type', 'NATIVE')
        result = unifiedorder.getResult()
        return result


class website_sale(http.Controller):
    @http.route(['/shop/payment/transaction/<int:acquirer_id>'],
                type='json', auth="public", website=True)
    def payment_transaction(self, acquirer_id):
        super(website_sale, self).payment_transaction(acquirer_id)
        tx = request.website.sale_get_transaction()
        acquirer = request.registry.get('payment.acquirer').browse(
            request.cr, request.uid, acquirer_id)
        if acquirer.provider == 'wcpay':
            weixin().set_wcpayconf(acquirer)
            result = weixin().connect_wcpay(request.cr, request.uid, tx)
            if result.get('return_code', None) == 'SUCCESS':
                pay_link = result.get('code_url', None)
                tx.wcpay_txn_paylink = pay_link
            else:
                _logger.warning('wcpay: %s' % result)
        return tx.id

    @http.route(['/shop/payment/transaction_so/<int:acquirer_id>'],
                type='json', auth="public", website=True)
    def payment_transaction_for_so(self, acquirer_id, sale_order_id=None):
        cr, context = request.cr, request.context
        transaction_obj = request.registry.get('payment.transaction')
        if sale_order_id is not None:
            request.session['sale_order_id'] = sale_order_id
        order = request.website.sale_get_order(context=context)

        if not order or not order.order_line or acquirer_id is None:
            return request.redirect("/shop/checkout")

        assert order.partner_id.id != request.website.partner_id.id

        tx = request.website.sale_get_transaction()
        if tx:
            tx_id = tx.id
        else:
            tx = order.payment_tx_id
            if tx:
                tx_id = tx.id
                request.session['sale_transaction_id'] = tx_id
                tx = request.website.sale_get_transaction()
            else:
                tx_id = transaction_obj.create(cr, SUPERUSER_ID, {
                    'acquirer_id': acquirer_id,
                    'type': 'form',
                    'amount': order.amount_total,
                    'currency_id': order.pricelist_id.currency_id.id,
                    'partner_id': order.partner_id.id,
                    'partner_country_id': order.partner_id.country_id.id,
                    'reference': order.name,
                    'sale_order_id': order.id,
                }, context=context)
                tx = transaction_obj.browse(cr, SUPERUSER_ID, tx_id)
                request.session['sale_transaction_id'] = tx_id

        # can not bind two more payment_method and workflow_process
        # update quotation
        request.registry['sale.order'].write(
            cr, SUPERUSER_ID, [order.id], {
                'payment_acquirer_id': acquirer_id,
                'payment_tx_id': tx_id
            }, context=context)

        acquirer = request.registry.get('payment.acquirer').browse(
            request.cr, request.uid, acquirer_id)
        if acquirer.provider == 'wcpay':
            weixin().set_wcpayconf(acquirer)
            result = weixin().connect_wcpay(request.cr, request.uid, tx)
            if result.get('return_code', None) == 'SUCCESS':
                pay_link = result.get('code_url', None)
                tx.wcpay_txn_paylink = pay_link
                tx.write({
                    'state': 'pending',
                })
            else:
                _logger.warning('wcpay: %s' % result)

        return tx_id

    @http.route(['/shop/payment/transaction_ai/<int:acquirer_id>'],
                type='json', auth="public", website=True)
    def payment_transaction_for_ai(self, acquirer_id, account_invoice_id=None):
        cr, context = request.cr, request.context
        transaction_obj = request.registry.get('payment.transaction')
        if account_invoice_id is not None:
            request.session['account_invoice_id'] = account_invoice_id
        invoice = request.registry['account.invoice'].browse(
            cr, SUPERUSER_ID, account_invoice_id, context=context)

        # if not invoice or not invoice.invoice_line or acquirer_id is None:
        #     return request.redirect("/shop/checkout")

        assert invoice.partner_id.id != request.website.partner_id.id

        tx = invoice.payment_tx_id
        if tx:
            tx_id = tx.id
            request.session['account_transaction_id'] = tx_id
        else:
            tx_id = transaction_obj.create(cr, SUPERUSER_ID, {
                'acquirer_id': acquirer_id,
                'type': 'form',
                'amount': invoice.residual,
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_country_id': invoice.partner_id.country_id.id,
                'reference': invoice.number,
                'account_invoice_id': invoice.id,
            }, context=context)
            tx = transaction_obj.browse(cr, SUPERUSER_ID, tx_id)
            request.session['account_transaction_id'] = tx_id

        # can not bind two more payment_method and workflow_process
        # update quotation
        request.registry['account.invoice'].write(
            cr, SUPERUSER_ID, [invoice.id], {
                'payment_acquirer_id': acquirer_id,
                'payment_tx_id': tx_id
            }, context=context)

        acquirer = request.registry.get('payment.acquirer').browse(
            request.cr, request.uid, acquirer_id)
        if acquirer.provider == 'wcpay':
            weixin().set_wcpayconf(acquirer)
            result = weixin().connect_wcpay(request.cr, request.uid, tx)
            if result.get('return_code', None) == 'SUCCESS':
                pay_link = result.get('code_url', None)
                tx.wcpay_txn_paylink = pay_link
                tx.write({
                    'state': 'pending',
                })
            else:
                _logger.warning('wcpay: %s' % result)

        return tx_id


class WcpayController(ReportController):
    _notify_url = '/payment/weixin/notify'
    _return_url = '/payment/weixin/return/'

    def kwargs_to_url(self, kwargs):
        res = ['%s=%s' % (args[0], args[1]) for args in kwargs.items()]
        return '&%s' % '&'.join(res)

    @route(['/report/barcode',
            '/report/barcode/<type>/<path:value>'], type='http', auth="public")
    def report_barcode(
            self, type, value, width=600, height=100, humanreadable=0,
            **kwargs):
        """Contoller able to render barcode images thanks to reportlab.
        Samples:
            <img t-att-src="'/report/barcode/QR/%s' % o.name"/>
            <img t-att-src="'/report/barcode/?type=%s&amp;value=%s&amp;
                width=%s&amp;height=%s' %
                ('QR', o.name, 200, 200)"/>

        :param type: Accepted types: 'Codabar', 'Code11', 'Code128', 'EAN13',
        'EAN8', 'Extended39', 'Extended93', 'FIM', 'I2of5', 'MSI', 'POSTNET',
        'QR', 'Standard39', 'Standard93',
        'UPCA', 'USPS_4State'
        :param humanreadable: Accepted values: 0 (default) or 1. 1 will insert
        the readable value at the bottom of the output image
        """
        value += self.kwargs_to_url(kwargs)
        return super(WcpayController, self).report_barcode(
            type, value, width=width, height=height,
            humanreadable=humanreadable)

    def _get_return_url(self, **post):
        """ Extract the return URL from the data coming from wcpay. """
        return self._return_url

    def wcpay_validate_data(self, xml):
        res = False
        wcpay_back = Wxpay_server_pub()
        wcpay_back.saveData(xml)
        data = wcpay_back.getData()
        if data.get('attach', None):
            # 生成签名时报错
            del data['attach']

        try:
            reference = data.get('out_trade_no')
        except Exception:
            reference = False

        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        if reference:
            tx_ids = request.registry['payment.transaction'].search(
                cr, uid, [('reference', '=', reference)], context=context)
            if tx_ids:
                request.registry['payment.transaction'].browse(
                    cr, uid, tx_ids[0], context=context)
        else:
            # should we create a payment transacation for wcpay
            _logger.warning(
                'wcpay: received wrong reference from wcpay: %s' % (
                    data.get('out_trade_no', '')))
            return res

        if wcpay_back.checkSign():
            _logger.info('wcpay: validated data')
            res = request.registry['payment.transaction'].form_feedback(
                cr, SUPERUSER_ID, data, 'wcpay', context=context)
        else:
            _logger.warning(
                'wcpay: received wrong md5str from wcpay: %s' % (
                    data.get('sign', '')))
        return res

    @http.route('/payment/weixin/notify', type='http', auth='none', methods=[
        'POST'])
    def weixin_notify(self, **post):
        xml = request.httprequest.data
        _logger.info(
            'Beginning wcpay AutoReceive form_feedback with post data %s',
            pprint.pformat(xml))
        res = self.wcpay_validate_data(xml)
        if res:
            return_code = 'SUCCESS'
            return_msg = 'OK'
        else:
            return_code = 'FAIL'
            return_msg = '签名失败'

        wc_return = Wxpay_server_pub()
        wc_return.setReturnParameter('return_code', return_code)
        wc_return.setReturnParameter('return_msg', return_msg)
        return_xml = wc_return.returnXml()
        return return_xml

    @http.route(['/shop/confirmation',
                 '/shop/confirmation/so/<int:sale_order_id>',
                 '/shop/confirmation/ai/<int:account_invoice_id>'],
                type='http', auth="public", website=True)
    def payment_confirmation(self, sale_order_id=None, account_invoice_id=None,
                             **post):
        cr, uid, context = request.cr, request.uid, request.context

        if post.get('subject'):
            subject = post.get('subject')
            sale_order_ids = request.registry['sale.order'].search(
                cr, uid, [('name', '=', subject)], context=context
            )
            if sale_order_ids:
                sale_order_id = sale_order_ids[0]

            if sale_order_id is None:
                account_invoice_ids = request.registry[
                    'account.invoice'].search(
                    cr, uid, [('number', '=', subject)], context=context
                )
                if account_invoice_ids:
                    account_invoice_id = account_invoice_ids[0]

        if (sale_order_id is None and
                account_invoice_id is None and
                request.session.uid and
                request.session.get('sale_last_order_id')):
            sale_order_id = request.session.get('sale_last_order_id')

        acquirer = request.registry['payment.acquirer'].search(
            cr, uid, [('name', '=', 'Wechat Pay')])

        if sale_order_id:
            order = request.registry['sale.order'].browse(
                cr, SUPERUSER_ID, sale_order_id, context=context)
            website_sale.payment_transaction_for_so(website_sale(),
                                                    acquirer[0],
                                                    order.id)
            return request.website.render("website_sale.confirmation",
                                          {'order': order})
        elif account_invoice_id:
            invoice = request.registry['account.invoice'].browse(
                cr, SUPERUSER_ID, account_invoice_id, context=context)
            website_sale.payment_transaction_for_ai(website_sale(),
                                                    acquirer[0],
                                                    invoice.id)
            return request.website.render("payment_wcpay.wcpay_confirmation",
                                          {'invoice': invoice})
        else:
            return request.redirect('/shop')

    @http.route('/shop/payment/get_status_so/<int:sale_order_id>',
                type='json',
                auth="public",
                website=True)
    def payment_get_status_so(self, sale_order_id, **post):
        cr, _, context = request.cr, request.uid, request.context
        order = request.registry['sale.order'].browse(cr, SUPERUSER_ID,
                                                      sale_order_id,
                                                      context=context)
        assert order.id == sale_order_id

        if not order:
            return {
                'state': 'error',
                'message': '<p>%s</p>' % _(
                    'There seems to be an error with your request.'),
            }
        else:
            tx_ids = request.registry['payment.transaction'].search(
                cr, SUPERUSER_ID,
                [
                    '|', ('sale_order_id', '=', order.id),
                    ('reference', '=', order.name),
                ], context=context)

        flag = False
        state = 'done'
        message = ""
        validation = None

        if not tx_ids:
            if order.amount_total:
                state = 'error'
                message = '<p>%s</p>' % _(
                    'There seems to be an error with your request.')
        else:
            pt = request.registry['payment.transaction']
            tx = pt.browse(cr, SUPERUSER_ID, tx_ids[0], context=context)
            state = tx.state
            flag = state == 'pending'
            if state == 'done':
                message = '<p>%s</p>' % _('Your payment has been received.')
            elif state == 'cancel':
                message = '<p>%s</p>' % _(
                    'The payment seems to have been canceled.')
            elif state == 'pending' and tx.acquirer_id.validation == 'manual':
                message = '<p>%s</p>' % _(
                    'Your transaction is waiting confirmation.')
                if tx.acquirer_id.post_msg:
                    message += tx.acquirer_id.post_msg
            elif state == 'error':
                message = '<p>%s</p>' % _(
                    'An error occurred during the transaction.')
            validation = tx.acquirer_id.validation

        return {
            'recall': flag,
            'state': state,
            'message': message,
            'validation': validation
        }

    @http.route('/shop/payment/get_status_ai/<int:account_invoice_id>',
                type='json', auth="public", website=True)
    def payment_get_status_ai(self, account_invoice_id, **post):
        cr, _, context = request.cr, request.uid, request.context
        invoice = request.registry['account.invoice'].browse(
            cr, SUPERUSER_ID, account_invoice_id, context=context)
        assert invoice.id == account_invoice_id

        if not invoice:
            return {
                'state': 'error',
                'message': '<p>%s</p>' % _(
                    'There seems to be an error with your request.'),
            }
        else:
            tx_ids = request.registry['payment.transaction'].search(
                cr, SUPERUSER_ID, [
                    '|', ('account_invoice_id', '=', invoice.id),
                    ('reference', '=', invoice.number)
                ], context=context)

        flag = False
        state = 'done'
        message = ""
        validation = None

        if not tx_ids:
            if invoice and invoice.residual:
                state = 'error'
                message = '<p>%s</p>' % _(
                    'There seems to be an error with your request.')
        else:
            pt = request.registry['payment.transaction']
            tx = pt.browse(cr, SUPERUSER_ID, tx_ids[0], context=context)
            state = tx.state
            flag = state == 'pending'
            if state == 'done':
                message = '<p>%s</p>' % _('Your payment has been received.')
            elif state == 'cancel':
                message = '<p>%s</p>' % _(
                    'The payment seems to have been canceled.')
            elif state == 'pending' and tx.acquirer_id.validation == 'manual':
                message = '<p>%s</p>' % _(
                    'Your transaction is waiting confirmation.')
                if tx.acquirer_id.post_msg:
                    message += tx.acquirer_id.post_msg
            elif state == 'error':
                message = '<p>%s</p>' % _(
                    'An error occurred during the transaction.')
            validation = tx.acquirer_id.validation

        return {
            'recall': flag,
            'state': state,
            'message': message,
            'validation': validation
        }
