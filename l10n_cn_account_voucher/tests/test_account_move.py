# -*- coding: utf-8 -*-
# © 2016 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
import logging
_logger = logging.getLogger(__name__)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TestAccountMove(common.TransactionCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()

        self.currency_usd_id = self.env.ref("base.USD").id
        self.account_account_1 = self.env['account.account'].create({
            'name': 'account_1',
            'code': 1111,
            'user_type_id': 4,
        })
        # currency_id is False
        self.account_move_line_1 = self.env['account.move.line'].create({
            'name': 'line_1',
            'journal_id': 1,
            'date': '2015-10-10',
            'date_maturity': '2015-10-10',
            'account_id': self.account_account_1.id,
            'currency_id': False,
        })
        # amount_currency is False and quantity is False
        self.account_move_line_2 = self.env['account.move.line'].create({
            'name': 'line_1',
            'journal_id': 1,
            'date': '2015-10-10',
            'date_maturity': '2015-10-10',
            'account_id': 1,
            'currency_id': 1,
            'amount_currency': False,
            'quantity': 0,
        })
        # amount_currency is True and debit > 0
        self.account_move_line_3 = self.env['account.move.line'].create({
            'name': 'line_1',
            'journal_id': 1,
            'date': '2015-10-10',
            'date_maturity': '2015-10-10',
            'account_id': 1,
            'currency_id': 1,
            'amount_currency': 2,
            'quantity': 10,
        })
        # amount_currency is True
        self.account_move_line_4 = self.env['account.move.line'].create({
            'name': 'line_1',
            'journal_id': 1,
            'date': '2015-10-10',
            'date_maturity': '2015-10-10',
            'account_id': 1,
            'currency_id': 1,
            'amount_currency': 1,
            'quantity': 10,
        })
        self.account_move_1 = self.env['account.move'].create({
            'name': '/',
            'journal_id': 1,
            'date': '2015-10-10',
            'line_ids': [(0, 0, {
                'name': 'foo',
                'debit': 10,
                'account_id': self.account_account_1.id,
            }), (0, 0, {
                'name': 'bar',
                'credit': 10,
                'account_id': self.account_account_1.id,
            })]
        })
        # amount_currency is True
        self.account_move_2 = self.env['account.move'].create({
            'name': '/',
            'journal_id': 1,
            'date': '2015-10-10',
            'line_ids': [(0, 0, {
                'name': 'foo2',
                'amount_currency': 10,
                'debit': 10,
                'currency_id': 1,
                'quantity': 2,
                'account_id': self.account_account_1.id,
            }), (0, 0, {
                'name': 'bar2',
                'amount_currency': -10,
                'credit': 10,
                'currency_id': 1,
                'quantity': 2,
                'account_id': self.account_account_1.id,
            })]
        })
        # debit > 0 and amount_currency is True
        self.line_1 = self.account_move_2.line_ids.search([
            ('name', '=', 'foo2')])
        # credit > 0 and amount_currency is True
        self.line_2 = self.account_move_2.line_ids.search([
            ('name', '=', 'bar2')])
        self.ir_property_1 = self.env['ir.property'].create({
            'fields_id': 1,
            'value_reference': 'account.account,1',
        })

    def test_paginate(self):
        """ Checks if the test_paginate works properly
        """
        res = self.account_move_1._paginate(self.account_move_1.line_ids)
        self.assertEqual(1, res)

    def test_get_account_name(self):
        """ Checks if the _get_account_name works properly
        """
        res = self.account_move_1._get_account_name(
            self.account_account_1.id)
        self.assertEqual('1111 account_1', res)

    def test_get_account_partner(self):
        """ Checks if the test_get_account_partner works properly
        """
        res = self.account_move_1._get_account_partner(1, 'name')
        self.assertEqual('name', res)
        res = self.account_move_1._get_account_partner(2, 'name')
        self.assertFalse(res)

    def test_get_exchange_rate(self):
        """ Checks if the _get_exchange_rate works properly
        """
        # amount_currency is False
        res = self.account_move_1._get_exchange_rate(self.account_move_line_2)
        self.assertEqual(0.0, res)
        # amount_currency is True and debit > 0
        res = self.account_move_2._get_exchange_rate(self.line_1)
        self.assertEqual(1.0, res)
        # amount_currency is True and credit > 0
        res = self.account_move_2._get_exchange_rate(self.line_2)
        self.assertEqual(1.0, res)

    def test_get_unit_price(self):
        """ Checks if the _get_unit_price works properly
        """
        # quantity is False
        res = self.account_move_1._get_unit_price(self.account_move_line_2)
        self.assertFalse(res)
        # quantity is True and debit > 0
        res = self.account_move_1._get_unit_price(self.line_1)
        self.assertEqual(5, res)
        # quantity is True and credit > 0
        res = self.account_move_1._get_unit_price(self.line_2)
        self.assertEqual(5, res)

    def test_rmb_format(self):
        """ Checks if the _rmb_format works properly
        """
        res = self.account_move_1._rmb_format(0.005)
        self.assertEqual(
            ['', '', '', '', '', '', '', '', '', '0', '0', '0'],
            res)
        res = self.account_move_1._rmb_format(1)
        self.assertEqual(
            ['', '', '', '', '', '', '', '', '', '1', '0', '0'], res)

    def test_rmb_upper(self):
        """ Checks if the test_rmb_upper works properly
        """
        res = self.account_move_1._rmb_upper(802.68)
        self.assertEqual(
            u'捌佰零贰元陆角捌分', res)
        res = self.account_move_1._rmb_upper(801)
        self.assertEqual(
            u'捌佰零壹元整', res)

    def test_compute_currency_rate(self):
        """ Checks if the _compute_currency_rate works properly
        """
        self.account_move_line_1._compute_currency_rate()
        self.assertFalse(self.account_move_line_2.currency_rate)
        self.assertEqual(
            self.account_move_line_3.currency_rate, abs(
                (self.account_move_line_3.debit
                    or self.account_move_line_3.credit) /
                self.account_move_line_3.amount_currency)
        )
