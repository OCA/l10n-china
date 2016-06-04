# -*- coding: utf-8 -*-
# © 2016 <matt.cai>cysnake4713@gmail.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class AccountMoveSequenceGenerationWizard(models.TransientModel):
    _name = 'account.move.sequence.generate.wizard'
    _rec_name = 'prefix'
    _description = 'Account Voucher Sequence Generation Wizard'

    prefix = fields.Char('Prefix Code', help="Prefix for the Voucher sequence", default='记')
    suffix = fields.Char('Suffix Code', help="Suffix for the Voucher sequence")
    number_begin = fields.Integer('Starting number', required=True, default=1, help="Begin number of Voucher")
    padding = fields.Integer('Sequence Padding', required=True, default=3,
                             help="Odoo will automatically adds some '0' on the left of the "
                                  "'Starting Number' to get the required padding size.")
    is_rewrite = fields.Boolean('Rewriting Existing Number?', default=False)
    has_sequence_move_ids = fields.Many2many('account.move', 'move_has_sequence_wizard_voucher_rel', 'wizard_id', 'move_id',
                                             string='Had Sequence Vouchers', readonly=True)
    empty_sequence_move_ids = fields.Many2many('account.move', 'move_empty_sequence_wizard_voucher_rel', 'wizard_id', 'move_id',
                                               string='No Sequence Vouchers', readonly=True)

    @api.model
    def default_get(self, fields_list):
        result = super(AccountMoveSequenceGenerationWizard, self).default_get(fields_list)
        if self._context.get('active_ids'):
            move_ids = self._context['active_ids']
            empty_seq_move_ids = self.env['account.move'].search([('id', 'in', move_ids), ('chinese_sequence_number', '=', False)]).ids
            has_seq_move_ids = self.env['account.move'].search([('id', 'in', move_ids), ('chinese_sequence_number', '!=', False)]).ids
            result['has_sequence_move_ids'] = has_seq_move_ids
            result['empty_sequence_move_ids'] = empty_seq_move_ids
        return result

    @api.multi
    def button_generate_number(self):
        format_string = (self.prefix or '') + '%0' + str(self.padding) + 'd' + (self.suffix or '')
        move_ids = self.empty_sequence_move_ids.ids
        if self.is_rewrite:
            move_ids += self.has_sequence_move_ids.ids
        number = self.number_begin
        for account_move in self.env['account.move'].search([('id', 'in', move_ids)], order='date asc, id asc'):
            account_move.chinese_sequence_number = format_string % number
            number += 1
