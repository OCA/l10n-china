# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import urlparse
from hashlib import md5

from openerp import SUPERUSER_ID
from ..controllers.main import AlipayController
from openerp.exceptions import except_orm
from openerp.osv import osv, fields
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class AcquirerAlipay(osv.Model):
    _inherit = 'payment.acquirer'

    def _get_alipay_urls(self, cr, uid, environment, context=None):
        """ Alipay URLs
        """
        return {
            'alipay_form_url': 'https://mapi.alipay.com/gateway.do',
        }

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerAlipay, self)._get_providers(
            cr, uid, context=context)
        providers.append(['alipay', 'Alipay'])
        return providers

    _columns = {
        'alipay_pid': fields.char('PID', required_if_provider='alipay'),
        'alipay_key': fields.char('Key', required_if_provider='alipay'),
        'alipay_seller_email': fields.char(
            'Seller Email', required_if_provider='alipay'),
        'logistics_type': fields.char(
            'Logistics Type', required_if_provider='alipay'),
        'logistics_fee': fields.char(
            'Logistics Fee', required_if_provider='alipay'),
        'logistics_payment': fields.char(
            'Logistics Payment', required_if_provider='alipay'),
        'service': fields.selection(
            [('create_direct_pay_by_user',
              'create_direct_pay_by_user'),
             ('create_partner_trade_by_buyer',
              'create_partner_trade_by_buyer'), ],
            'Payment Type',
            default='create_direct_pay_by_user',
            required_if_provider='alipay'
        ),
    }

    def _check_payment_type(self, cr, uid, ids, context=None):
        payment_ids = self.read(
            cr, uid, ids, ['service', 'provider'], context=context)
        for payment in payment_ids:
            if payment['provider'] == 'alipay' and not payment['service']:
                return False
        return True

    _constraints = [
        (
            _check_payment_type,
            'Payment type is NULL.', ['service']
        )
    ]

    def _alipay_generate_md5_sign(self, acquirer, inout, values):
        """ Generate the md5sign for incoming or outgoing communications.

        :param browse acquirer: the payment.acquirer browse record. It should
                                have a md5key in shaky out
        :param string inout: 'in' (openerp contacting alipay) or 'out' (alipay
                             contacting openerp).
        :param dict values: transaction values

        :return string: md5sign
        """
        assert inout in ('in', 'out')
        assert acquirer.provider == 'alipay'
        try:
            assert acquirer.alipay_key
        except Exception, e:
            _logger.exception(e)
            raise except_orm(_(
                "the acquirer model %s alipay_key can not be null"
                % acquirer), _(e))
        alipay_key = acquirer.alipay_key

        # TODO: raise error or use empty string?
        src = ''
        filter_keys = ['sign', 'sign_type']
        if inout == 'out':
            if not values.get('is_success', ''):
                src = '&'.join(
                    ['%s=%s' % (key, value)
                        for key, value in sorted(values.items())
                        if key not in filter_keys]) + alipay_key
            else:
                src = '&'.join(
                    ['%s=%s' % (key, value)
                        for key, value in sorted(values.items())
                        if key not in filter_keys]) + alipay_key
        else:
            if values.get('service', '') == 'create_direct_pay_by_user':
                src = '&'.join(
                    ['%s=%s' % (key, value)
                        for key, value in sorted(values.items())
                        if key not in filter_keys]) + alipay_key
            elif values.get('service', '') == 'create_partner_trade_by_buyer':
                src = '&'.join(
                    ['%s=%s' % (key, value)
                        for key, value in sorted(values.items())
                        if key not in filter_keys]) + alipay_key
        return md5(src.encode('utf-8')).hexdigest()

    def alipay_form_generate_values(
            self, cr, uid, id, partner_values, tx_values,
            context=None
    ):
        """
        source code need return a tuple
        if use new API, it will wrap to list, like [tuple] and cause a error.
        :param cr:
        :param uid:
        :param id:
        :param partner_values:
        :param tx_values:
        :param context:
        :return:
        """
        base_url = self.pool['ir.config_parameter'].get_param(
            cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)

        alipay_tx_values = dict(tx_values)
        alipay_tx_values.update({
            'seller_email': acquirer.alipay_seller_email,
            '_input_charset': 'utf-8',
            'partner': acquirer.alipay_pid,
            'payment_type': '1',
            'service': acquirer.service,
            'sign_type': 'MD5',
            'out_trade_no': tx_values['reference'],
            'total_fee': tx_values['amount'],
            'subject': tx_values['reference'],
            'price': tx_values['amount'],
            'quantity': '1',
            'is_success': 'T',
            'logistics_fee': acquirer.logistics_fee,
            'logistics_payment': acquirer.logistics_payment,
            'logistics_type': acquirer.logistics_type,
            'return_url': '%s' % urlparse.urljoin(
                base_url, AlipayController._return_url),
            'notify_url': '%s' % urlparse.urljoin(
                base_url, AlipayController._notify_url),
            'cancel_return': '%s' % urlparse.urljoin(
                base_url, AlipayController._cancel_url),
        })
        alipay_tx_values['sign'] = self._alipay_generate_md5_sign(
            acquirer, 'in', alipay_tx_values)
        return partner_values, alipay_tx_values

    def alipay_get_form_action_url(self, cr, uid, id, context=None):
        acquirer = self.browse(cr, uid, id, context=context)
        return self._get_alipay_urls(
            cr, uid, acquirer.environment, context=context)['alipay_form_url']
