import urlparse

from openerp.addons.edi import EDIMixin
from werkzeug import url_encode

from openerp import models, api, fields
from ..controllers.main import AlipayController


class AccountInvoice(models.Model, EDIMixin):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('name', 'residual')
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
                    'out_trade_no': self.number,
                    'subject': self.number,
                    'total_fee': self.residual,
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
        compute='_edi_alipay_url_direct_pay', string='Alipay Url Direct Pay')

    def action_invoice_sent(self, cr, uid, ids, context=None):
        """Override to use a modified template that includes a portal signup
        link """
        action_dict = super(AccountInvoice, self) \
            .action_invoice_sent(cr, uid, ids, context=context)
        try:
            template_id = self.pool.get('ir.model.data') \
                .get_object_reference(cr,
                                      uid,
                                      'payment_alipay',
                                      'email_template_edi_invoice')[1]
            # assume context is still a dict, as prepared by super
            ctx = action_dict['context']
            ctx['default_template_id'] = template_id
            ctx['default_use_template'] = True
        except Exception:
            pass
        return action_dict
