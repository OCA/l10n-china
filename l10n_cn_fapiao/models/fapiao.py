# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class fapiao(models.Model):
    _name = "fapiao"
    _inherit = 'mail.thread'
    _order = "fapiao_date desc"

    fapiao_type = fields.Selection(
        [('customer', 'Customer'), ('supplier', 'Supplier'),
         ('customer_credit_note', 'Customer Credit note')],
        'Fapiao Type', required=True, default='customer')
    tax_type = fields.Selection(
        [('13%', '13%'), ('17%', '17%'),
         ('normal', 'normal'), ('no_tax', 'no tax')],
        'Tax Type', required=True, default='normal')
    fapiao_number = fields.Integer(string="Fapiao Number", required=True)
    fapiao_date = fields.Date(string="Fapiao Date", required=True)
    reception_date = fields.Date(string="Reception Date")
    amount_with_taxes = fields.Float('Fapiao total amount', required=True)
    invoice_ids = fields.Many2many('account.invoice', string="Invoices")
    tag_ids = fields.Many2many('fapiao_tag', string="Tags")
    notes = fields.Text(string="Notes")


class fapiao_tag(models.Model):
    _name = 'fapiao_tag'

    name = fields.Char("Name")


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    fapiao_ids = fields.Many2many('fapiao', string='Fapiao')
