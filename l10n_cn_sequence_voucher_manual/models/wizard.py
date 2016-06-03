# coding=utf-8
"""
author: matt.cai(cysnake4713@gmail.com)
"""
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class AccountMoveSequenceGenerateWizard(models.TransientModel):
    _name = 'account.move.sequence.generate.wizard'
    _rec_name = 'prefix'
    _description = 'Account Voucher Sequence Generate Wizard'

    prefix = fields.Char('Prefix Code', help="Prefix value of the record for the Voucher sequence", default='记')
    suffix = fields.Char('Suffix Code', help="Suffix value of the record for the Voucher")
    number_begin = fields.Integer('Begin Number', required=True, default=1, help="Begin number of Voucher")
    padding = fields.Integer('Sequence Size', required=True, default=3,
                             help="Odoo will automatically adds some '0' on the left of the "
                                  "'Begin Number' to get the required padding size.")
    is_rewrite = fields.Boolean('Rewrite Exist Number?', default=False)
    has_sequence_move_ids = fields.Many2many('account.move', 'move_has_sequence_wizard_voucher_rel', 'wizard_id', 'move_id',
                                             string='Had Sequence Vouchers', readonly=True)
    empty_sequence_move_ids = fields.Many2many('account.move', 'move_empty_sequence_wizard_voucher_rel', 'wizard_id', 'move_id',
                                               string='No Sequence Vouchers', readonly=True)

    @api.model
    def default_get(self, fields_list):
        result = super(AccountMoveSequenceGenerateWizard, self).default_get(fields_list)
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
