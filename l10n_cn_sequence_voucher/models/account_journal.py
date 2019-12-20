# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    internal_sequence_transfer_id = fields.Many2one(
        'ir.sequence', 'Transfer Sequence',
        help='''This sequence will be used to maintain the internal number
        for the journal entries related to this journal for transfer.'''
    )
    internal_sequence_out_id = fields.Many2one(
        'ir.sequence', 'Out Sequence',
        help='''This sequence will be used to maintain the internal number
        for the journal entries related to this journal
        for cash/bank in or out.'''
    )
    internal_sequence_in_id = fields.Many2one(
        'ir.sequence', 'IN Sequence',
        help='''This sequence will be used to maintain the internal number
        for the journal entries related to this journal
        for cash/bank in or out.'''
    )
