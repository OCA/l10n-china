# -*- coding: utf-'8' "-*-"

try:
    import simplejson as json
except ImportError:
    import json
import logging
import urlparse
from urllib import urlencode
import datetime

from openerp.osv import osv
from openerp import SUPERUSER_ID
from openerp import fields, api

import util
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.addons.payment_weixin.controllers.main import weixinController

_logger = logging.getLogger(__name__)


class AcquirerWeixin(osv.Model):
    _inherit = 'payment.acquirer'

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerWeixin, self)._get_providers(cr, uid, context=context)
        providers.append(['weixin', 'weixin'])
        return providers

    _columns = {
        'weixin_appid': fields.char('Weixin AppID', required_if_provider='weixin'),
        'weixin_paySignKey': fields.char('Wexin PaySignKey', required_if_provider='weixin'),
        'weixin_appSecret': fields.char('Wexin AppSecret', required_if_provider='weixin'),
        'weixin_partnerId': fields.char('Wexin Partner ID', required_if_provider='weixin'),
        'weixin_partnerKey': fields.char('Weixin Partner Key', required_if_provider='weixin'),
    }

    @api.one
    def _get_weixin_appid(self):
        return self.weixin_appid

    _defaults = {
        'fees_active': False,
    }

    def _get_weixin_urls(self, cr, uid, environment, context=None):
        return {
            'weixin_url': 'weixin://wxpay/bizpayurl?'
        }

    def weixin_form_generate_values(self, cr, uid, id, partner_values, tx_values, context=None):
        base_url = self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)
        amount = int(tx_values.get('total_fee', 0) * 100)
        time = datetime.datetime.now()
        noncestr = 'kskakkaj1999999999'

        weixin_tx_values = dict(tx_values)
        weixin_tx_values.update({
            'appid': acquirer.weixin_appid,
            'product_id': tx_values['reference'],
            'timestamp': time,
            'noncestr': noncestr,
        })

        to_sign = {}
        to_sign.update({
            'appid': acquirer.weixin_partner_account,
            'productid': tx_values['reference'],
            'timestamp': time,
            'noncestr': noncestr,
            'appkey': acquirer.weixin_paySignKey,
        })
        _, prestr = util.params_filter(to_sign)
        weixin_tx_values['sign'] = util.build_mysign(prestr, acquirer.weixin_partner_key, 'MD5')
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
