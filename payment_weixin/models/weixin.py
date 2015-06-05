# -*- coding: utf-'8' "-*-"

try:
    import simplejson as json
except ImportError:
    import json
import logging
import urlparse
import datetime

from openerp.osv import osv
from openerp import SUPERUSER_ID
from openerp import fields

import util
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.http import request

_logger = logging.getLogger(__name__)


class AcquirerWeixin(osv.Model):
    _inherit = 'payment.acquirer'

    @api.one
    def _get_ipaddress(self):
        return request.httprequest.environ['REMOTE_ADDR']

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerWeixin, self)._get_providers(cr, uid, context=context)
        providers.append(['weixin', 'weixin'])
        return providers

    _columns = {
        'weixin_appid': fields.char('APPID', required_if_provider='weixin'),
        'weixin_mch_id': fields.char(u'微信支付商户号', required_if_provider='weixin'),
        'weixin_key': fields.char(u'API密钥', required_if_provider='weixin'),
        'weixin_secret': fields.char('Appsecret', required_if_provider='weixin'),
    }

    def _get_weixin_urls(self, cr, uid, environment, context=None):
        """ Weixin URLS """
        if environment == 'prod':
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }
        else:
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }

    _defaults = {
        'fees_active': False,
    }

    def weixin_form_generate_values(self, cr, uid, id, partner_values, tx_values, context=None):
        base_url = self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)
        amount = int(tx_values.get('total_fee', 0) * 100)
        noncestr = 'kskakkaj1999999999'

        weixin_tx_values = dict(tx_values)
        weixin_tx_values.update({
            'appid': acquirer.weixin_appid,
            'mch_id': acquirer.weixin_mch_id,
            'noncestr': noncestr,
            'body': tx_values['reference'],
            'out_trade_no': tx_values['reference'],
            'total_fee': amount,
            'spbill_create_ip': acquirer._get_ipaddress(),
            'notify_url': '%s' % urlparse.urljoin(base_url, WexinController._notify_url),
            'trade_type': 'NATIVE',
            'product_id': tx_values['reference'],

        })

        _, prestr = util.params_filter(weixin_tx_values)
        weixin_tx_values['sign'] = util.build_mysign(prestr, acquirer.weixin_key, 'MD5')
        return partner_values, weixin_tx_values

    def weixin_get_form_action_url(self, cr, uid, id, context=None):
        acquirer = self.browse(cr, uid, id, context=context)
        return self._get_weixin_urls(cr, uid, acquirer.environment, context=context)['weixin_url']


class TxWeixin(osv.Model):
    _inherit = 'payment.transaction'

    _columns = {
        'weixin_txn_id': fields.char('Transaction ID'),
        'weixin_txn_type': fields.char('Transaction type'),
    }

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    def _weixin_form_get_tx_from_data(self, cr, uid, data, context=None):
        reference, txn_id = data.get('out_trade_no'), data.get('out_trade_no')
        if not reference or not txn_id:
            error_msg = 'weixin: received data with missing reference (%s) or txn_id (%s)' % (reference, txn_id)
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        tx_ids = self.pool['payment.transaction'].search(cr, uid, [('reference', '=', reference)], context=context)
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'weixin: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return self.browse(cr, uid, tx_ids[0], context=context)

    def _weixin_form_validate(self, cr, uid, tx, data, context=None):
        status = data.get('trade_state')
        data = {
            'acquirer_reference': data.get('out_trade_no'),
            'weixin_txn_id': data.get('out_trade_no'),
            'weixin_txn_type': data.get('fee_type'),

        }

        if status == 0:
            _logger.info('Validated weixin payment for tx %s: set as done' % (tx.reference))
            data.update(state='done', date_validate=data.get('time_end', fields.datetime.now()))
            return tx.write(data)

        else:
            error = 'Received unrecognized status for weixin payment %s: %s, set as error' % (tx.reference, status)
            _logger.info(error)
            data.update(state='error', state_message=error)
            return tx.write(data)
