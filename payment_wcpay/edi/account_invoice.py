from openerp.addons.edi import EDIMixin

from openerp import models, api, fields


class AccountInvoice(models.Model, EDIMixin):
    _inherit = 'account.invoice'

    payment_acquirer_id = fields.Many2one(
        comodel_name='payment.acquirer',
        string='Payment Acquirer'
    )

    payment_tx_id = fields.Many2one(
        comodel_name='payment.transaction',
        string='Payment transaction'
    )

    @api.one
    @api.depends('name', 'residual')
    def _edi_wcpay_url_direct_pay(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        self.wcpay_url_direct_pay = \
            '%s/shop/confirmation/ai/%s' % (base_url, self.id)

    wcpay_url_direct_pay = fields.Char(
        compute='_edi_wcpay_url_direct_pay',
        string='Wcpay Url Direct Pay')
