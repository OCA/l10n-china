# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
import logging
import pprint
import urllib2
import werkzeug

from lxml import etree

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.addons.payment_weixin.models import util

_logger = logging.getLogger(__name__)


class WeixinController(http.Controller):
    _notify_url = '/payment/weixin/notify/'

    def weixin_validate_data(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        json = {}
        for el in etree.fromstring(post):
            json[el.tag] = el.text

        _KEY = request.registry['payment.acquirer']._get_weixin_key()
        _, prestr = util.params_filter(json)
        mysign = util.build_mysign(prestr, _KEY, 'MD5')
        if mysign != json.get('sign'):
            return 'false'

        _logger.info('weixin: validated data')
        return request.registry['payment.transaction'].form_feedback(cr, SUPERUSER_ID, json, 'weixin',
                                                                     context=context)

    @http.route('/payment/weixin/notify', type='http', auth='none', methods=['POST'])
    def weixin_notify(self, **post):
        """ weixin Notify. """
        _logger.info('Beginning weixin notify form_feedback with post data %s', pprint.pformat(post))  # debug
        if self.weixin_validate_data(**post):
            return 'success'
        else:
            return ''
