# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import urlparse

from openerp import models, api, fields
from openerp.addons.edi import EDIMixin
from ..controllers.main import AlipayController
from werkzeug import url_encode


class SaleOrder(models.Model, EDIMixin):
    _inherit = 'sale.order'

    @api.one
    @api.depends('name', 'amount_total')
    def _edi_alipay_url_direct_pay(self):
        acquirer_objs = self.env['payment.acquirer'].search([
            ('provider', '=', 'alipay'),
            ('website_published', '=', True)])
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        for acquirer in acquirer_objs:
            if acquirer and self.state not in ['cancel', 'draft', 'done']:
                params = {
                    'return_url': '%s' % urlparse.urljoin(
                        base_url, AlipayController._return_url),
                    'notify_url': '%s' % urlparse.urljoin(
                        base_url, AlipayController._notify_url),
                    '_input_charset': 'utf-8',
                    'partner': acquirer.alipay_pid,
                    'payment_type': '1',
                    'seller_email': acquirer.alipay_seller_email,
                    'service': acquirer.service,
                    'out_trade_no': self.name,
                    'subject': self.name,
                    'total_fee': self.amount_total,
                    'sign_type': 'MD5',
                    'is_success': 'T'
                }
                params['sign'] = acquirer._alipay_generate_md5_sign(
                    acquirer, 'in', params)
                if acquirer.service == 'create_direct_pay_by_user':
                    self.alipay_url_direct_pay = '%s%s%s' % (
                        acquirer.alipay_get_form_action_url()[0],
                        '?', url_encode(params))

    alipay_url_direct_pay = fields.Char(
        compute='_edi_alipay_url_direct_pay',
        string='Alipay Url Direct Pay'
    )

    def action_quotation_send(self, cr, uid, ids, context=None):
        """
        Override to use a modified template that includes a portal signup link
        :param cr:
        :param uid:
        :param ids:
        :param context:
        :return:
        """
        action_dict = super(SaleOrder, self) \
            .action_quotation_send(cr, uid, ids,
                                   context=context)
        try:
            template_id = \
                self.pool.get('ir.model.data') \
                    .get_object_reference(cr, uid,
                                          'payment_alipay',
                                          'email_template_edi_sale')[1]
            # assume context is still a dict, as prepared by super
            ctx = action_dict['context']
            ctx['default_template_id'] = template_id
            ctx['default_use_template'] = True
        except Exception:
            pass
        return action_dict
