# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    chinese_sequence_type = fields.Selection([
        ('cash_in', '现收'), ('cash_out', '现付'),
        ('bank_in', '银收'), ('bank_out', '银付'),
        ('transfer', '转')],
        'Voucher Type change to',
        help='Internal Sequence Type')
    chinese_sequence_number = fields.Char(
        'Chinese Voucher Number', size=64, copy=False,
        readonly=True, help='Internal Sequence Number')

    @api.multi
    def write(self, vals):
        c = self.env.context.copy()
        c['novalidate'] = True
        if 'state' in vals and vals['state'] == 'posted':
            for move in self:
                if not move.chinese_sequence_number:
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_transfer')[0]
                    seq_no = sequence_id.next_by_id()
                    if seq_no:
                        vals['chinese_sequence_number'] = seq_no
        result = super(AccountMove, self).write(vals)
        return result

    @api.multi
    def post(self):
        obj_sequence = self.env['ir.sequence']
        res = super(AccountMove, self).post()
        seq_no = False
        for move in self:
            if move.chinese_sequence_type:
                if move.chinese_sequence_type == 'cash_in':
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_cash_in')[0]
                if move.chinese_sequence_type == 'cash_out':
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_cash_out')[0]
                if move.chinese_sequence_type == 'bank_in':
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_bank_in')[0]
                if move.chinese_sequence_type == 'bank_out':
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_bank_out')[0]
                if move.chinese_sequence_type == 'transfer':
                    sequence_id = self.env.ref(
                        'l10n_cn_sequence_voucher\
.sequence_journal_seq_transfer')[0]
                seq_no = sequence_id.next_by_id()
                if seq_no:
                    res = self.write({'chinese_sequence_number': seq_no})
            else:
                for line in move.line_ids:
                    if line.account_id.code == '1001.01':
                        if line.credit != 0 and line.debit == 0:
                            if move.journal_id.internal_sequence_out_id:
                                sequence_id = obj_sequence.browse(
                                    move.journal_id.
                                    internal_sequence_out_id.id)
                                seq_no = sequence_id.next_by_id()
                        if line.credit == 0 and line.debit != 0:
                            if move.journal_id.internal_sequence_in_id:
                                sequence_id = obj_sequence.browse(
                                    move.journal_id.
                                    internal_sequence_in_id.id)
                                seq_no = sequence_id.next_by_id()
                    if line.account_id.code == '1002.01':
                        if line.credit != 0 and line.debit == 0:
                            if move.journal_id.internal_sequence_out_id:
                                sequence_id = obj_sequence.browse(
                                    move.journal_id.
                                    internal_sequence_out_id.id)
                                seq_no = sequence_id.next_by_id()
                        if line.credit == 0 and line.debit != 0:
                            if move.journal_id.internal_sequence_in_id:
                                sequence_id = obj_sequence.browse(
                                    move.journal_id.
                                    internal_sequence_in_id.id)
                                seq_no = sequence_id.next_by_id()
                    if seq_no:
                        res = self.write({
                            'chinese_sequence_number': seq_no})
                        break
                if not seq_no:
                    if move.journal_id.internal_sequence_transfer_id:
                        seq_no = obj_sequence.browse(
                            move.journal_id.internal_sequence_transfer_id.id).\
                            next_by_id()
                    if seq_no:
                        res = self.write({'chinese_sequence_number': seq_no})
        return res
