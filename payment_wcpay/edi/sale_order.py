from openerp.addons.edi import EDIMixin

from openerp import models, api, fields


class SaleOrder(models.Model, EDIMixin):
    _inherit = 'sale.order'

    @api.one
    @api.depends('name', 'amount_total')
    def _edi_wcpay_url_direct_pay(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        self.wcpay_url_direct_pay = \
            '%s/shop/confirmation/so/%s' % (base_url, self.id)

    wcpay_url_direct_pay = fields.Char(
        compute='_edi_wcpay_url_direct_pay',
        string='Wcpay Pay Url Direct Pay'
    )
