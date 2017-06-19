# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fapiao_ids = fields.Many2many('fapiao', string='Fapiao')
