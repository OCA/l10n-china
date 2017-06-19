# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class fapiao(models.Model):
    _name = 'fapiao'
    _inherit = 'mail.thread'
    _order = 'fapiao_date desc'

    def _default_tax_type(self):
        return self.env['fapiao.tax.type'].search([('name', '=', 'normal')])

    fapiao_type = fields.Selection(
        [('customer', 'Customer'),
         ('supplier', 'Supplier'),
         ('customer_credit_note', 'Customer Credit note')],
        'Fapiao Type',
        required=True,
        default='customer')
    tax_type = fields.Many2one('fapiao.tax.type',
                               string='Tax Type',
                               required=True,
                               default=_default_tax_type)
    fapiao_number = fields.Integer(string='Fapiao Number', required=True)
    fapiao_date = fields.Date(string='Fapiao Date', required=True)
    reception_date = fields.Date(string='Reception Date')
    amount_with_taxes = fields.Float('Fapiao total amount', required=True)
    invoice_ids = fields.Many2many('account.invoice', string='Invoices')
    tag_ids = fields.Many2many('fapiao.tag', string='Tags')
    notes = fields.Text(string='Notes')
