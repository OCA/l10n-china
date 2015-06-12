# -*- coding: utf-'8' "-*-"
from  openerp.addons.payment_weixini.controllers.main import WeixinController

try:
    import simplejson as json
except ImportError:
    import json
import logging
import urlparse
import urllib2
from lxml import etree

from openerp.osv import osv
from openerp import SUPERUSER_ID

import util
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.http import request
from openerp import api, fields, models

_logger = logging.getLogger(__name__)


class AcquirerWeixin(models.Model):
    _inherit = 'payment.acquirer'

    def _get_ipaddress(self):
        return request.httprequest.environ['REMOTE_ADDR']

    @api.model
    def _get_providers(self):
        providers = super(AcquirerWeixin, self)._get_providers()
        providers.append(['weixin', 'weixin'])
        return providers

    weixin_appid = fields.Char(string='Weixin APPID', required_if_provider='weixin')
    weixin_mch_id = fields.Char(string=u'微信支付商户号', required_if_provider='weixin')
    weixin_key = fields.Char(string=u'API密钥', required_if_provider='weixin')
    weixin_secret = fields.Char(string='Weixin Appsecret', required_if_provider='weixin')

    def _get_weixin_urls(self, environment):
        if environment == 'prod':
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }
        else:
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }

    @api.one
    def _get_weixin_key(self):
        return self.weixin_key

    _defaults = {
        'fees_active': False,
    }

    def json2xml(self, json):
        string = ""
        for k, v in json.items():
            string = string + "<%s>" % (k) + str(v) + "</%s>" % (k)

        return string

    def _try_url(self, request, tries=3, context=None):

        done, res = False, None
        while (not done and tries):
            try:
                res = urllib2.urlopen(request)
                done = True
            except urllib2.HTTPError as e:
                res = e.read()
                e.close()
                if tries and res and json.loads(res)['name'] == 'INTERNAL_SERVICE_ERROR':
                    _logger.warning('Failed contacting Paypal, retrying (%s remaining)' % tries)
            tries = tries - 1
        if not res:
            pass
            # raise openerp.exceptions.
        result = res.read()
        res.close()
        return result

    @api.multi
    def weixin_form_generate_values(self, partner_values, tx_values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        amount = int(tx_values.get('total_fee', 0) * 100)
        noncestr = 'kskakkaj1999999999'

        weixin_tx_values = dict(tx_values)
        weixin_tx_values.update(
            {
                'appid': self.weixin_appid,
                'mch_id': self.weixin_mch_id,
                'noncestr': noncestr,
                'body': tx_values['reference'],
                'out_trade_no': tx_values['reference'],
                'total_fee': amount,
                'spbill_create_ip': self._get_ipaddress(),
                'notify_url': '%s' % urlparse.urljoin(base_url, WeixinController._notify_url),
                'trade_type': 'NATIVE',
                'product_id': tx_values['reference'],

            }
        )

        data_post = {}
        data_post.update(
            {
                'appid': self.weixin_appid,
                'mch_id': self.weixin_mch_id,
                'noncestr': noncestr,
                'body': tx_values['reference'],
                'out_trade_no': tx_values['reference'],
                'total_fee': amount,
                'spbill_create_ip': self._get_ipaddress(),
                'notify_url': '%s' % urlparse.urljoin(base_url, WeixinController._notify_url),
                'trade_type': 'NATIVE',
                'product_id': tx_values['reference'],

            }

        )

        _, prestr = util.params_filter(data_post)
        weixin_tx_values['sign'] = util.build_mysign(prestr, self.weixin_key, 'MD5')
        data_post['sign'] = weixin_tx_values['sign']

        data_xml = "<xml>" + self.json2xml(data_post) + "</xml>"

        url = self._get_weixin_urls(self.environment)['weixin_url']

        request = urllib2.Request(url, data_xml)
        result = self._try_url(request, tries=3)
        return_xml = etree.fromstring(result)
        if return_xml.find('return_code').text == "SUCCESS" and return_xml.find('code_url').text <> False:
            qrcode = return_xml.find('code_url').text
            weixin_tx_values['qrcode'] = qrcode
        else:
            error_msg = "can not generate payment preparation ! please check the weixin account and settigns. "
            raise ValidationError(error_msg)

        return partner_values, weixin_tx_values

    @api.multi
    def weixin_get_form_action_url(self):
        self.ensure_one()
        return self._get_weixin_urls(self.environment)['weixin_url']


class TxWeixin(models.Model):
    _inherit = 'payment.transaction'

    weixin_txn_id = fields.Char(string='Transaction ID')
    weixin_txn_type = fields.Char(string='Transaction type')


    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    def _weixin_form_get_tx_from_data(self, data):
        reference, txn_id = data.get('out_trade_no'), data.get('out_trade_no')
        if not reference or not txn_id:
            error_msg = 'weixin: received data with missing reference (%s) or txn_id (%s)' % (reference, txn_id)
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        tx_ids = self.search([('reference', '=', reference)])
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'weixin: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx_ids[0]

    def _weixin_form_validate(self, tx, data):
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
