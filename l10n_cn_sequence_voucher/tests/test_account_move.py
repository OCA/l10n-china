# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
import logging
_logger = logging.getLogger(__name__)


class TestAccountMove(common.TransactionCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.account_move = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.account = self.env['account.account'].create({
            'name': 'account_1',
            'code': '9000.00',
            'user_type_id': 4})
        # code == '1001.01'
        self.account1 = self.env['account.account'].create({
            'name': 'account_1',
            'code': '1001.01',
            'user_type_id': 4})
        self.account2 = self.env['account.account'].create({
            'name': 'account_1',
            'code': '1002.01',
            'user_type_id': 4})
        self.account_move1 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': 'cash_in',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.account_move2 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': 'cash_out',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.account_move3 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': 'bank_in',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.account_move4 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': 'bank_out',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.account_move5 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': 'transfer',
            'line_ids': [
                [0, 0, {'account_id': 1, 'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        self.sequence = self.env['ir.sequence'].create({
            'name': 'sequence_1'
        })
        # internal_sequence_out_id is True
        self.journal_1 = self.env['account.journal'].create({
            'name': 'journal_1',
            'type': 'bank',
            'internal_sequence_out_id': 1,
        })
        # internal_sequence_in_id is True
        self.journal_2 = self.env['account.journal'].create({
            'name': 'journal_2',
            'type': 'bank',
            'internal_sequence_in_id': 1,
        })
        self.account_move6 = self.env['account.move'].create({
            'journal_id': 1,
            'date': '2015-10-10',
            'chinese_sequence_type': False,
            'line_ids': [
                [0, 0, {
                    'account_id': self.account1.id,
                    'name': 'test', 'credit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'debit': 10}]
            ]})
        # account code = 1001.01
        self.account_move7 = self.env['account.move'].create({
            'journal_id': self.journal_1.id,
            'date': '2015-10-10',
            'chinese_sequence_type': False,
            'line_ids': [
                [0, 0, {
                    'account_id': self.account1.id,
                    'name': 'test', 'debit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'credit': 10}]
            ]})
        # account code = 1001.01
        self.account_move8 = self.env['account.move'].create({
            'journal_id': self.journal_2.id,
            'date': '2015-10-10',
            'chinese_sequence_type': False,
            'line_ids': [
                [0, 0, {
                    'account_id': self.account1.id,
                    'name': 'test', 'credit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'debit': 10}]
            ]})
        # account code = 1002.01
        self.account_move9 = self.env['account.move'].create({
            'journal_id': self.journal_1.id,
            'date': '2015-10-10',
            'chinese_sequence_type': False,
            'line_ids': [
                [0, 0, {
                    'account_id': self.account2.id,
                    'name': 'test', 'credit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'debit': 10}]
            ]})
        # account code = 1002.01
        self.account_move10 = self.env['account.move'].create({
            'journal_id': self.journal_2.id,
            'date': '2015-10-10',
            'chinese_sequence_type': False,
            'line_ids': [
                [0, 0, {
                    'account_id': self.account2.id,
                    'name': 'test', 'credit': 10}],
                [0, 0, {'account_id': 2, 'name': 'test_2', 'debit': 10}]
            ]})

    def test_write(self):
        """ Checks if the test_write works properly
        """
        vals = {
        }
        self.account_move.write(vals)
        self.assertFalse(vals.get('chinese_sequence_number', ''))
        vals = {
            'state': 'posted'
        }
        self.account_move.write(vals)
        self.assertTrue(vals.get('chinese_sequence_number', ''))

    def test_post(self):
        """ Checks if the test_post works properly
        """
        self.account_move1.post()
        self.assertTrue(self.account_move1.chinese_sequence_number, '')
        self.account_move2.post()
        self.assertTrue(self.account_move2.chinese_sequence_number, '')
        self.account_move3.post()
        self.assertTrue(self.account_move3.chinese_sequence_number, '')
        self.account_move4.post()
        self.assertTrue(self.account_move4.chinese_sequence_number, '')
        self.account_move5.post()
        self.assertTrue(self.account_move5.chinese_sequence_number, '')
        # chinese_sequence_type is False
        self.account_move6.post()
        self.assertTrue(self.account_move6.chinese_sequence_number, '')
        self.account_move7.post()
        self.assertTrue(self.account_move7.chinese_sequence_number, '')
        self.account_move8.post()
        self.assertTrue(self.account_move8.chinese_sequence_number, '')
        self.account_move9.post()
        self.assertTrue(self.account_move8.chinese_sequence_number, '')
        self.account_move10.post()
        self.assertTrue(self.account_move8.chinese_sequence_number, '')
