# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


class TestFapiao(common.TransactionCase):
    def setUp(self):
        super(TestFapiao, self).setUp()
        self.fapiao_tag_1 = self.env['fapiao_tag'].create({
            'name': 'FT1',
        })
        self.fapiao_tag_2 = self.env['fapiao_tag'].create({
            'name': 'FT2',
        })
        inv1 = {
            'name': 'i-v-1',
            'type': 'in_invoice',
            'number': '299048',
            'comment': '299048',
            'state': 'draft',
            'date': '2017-02-10',
            'date_invoice': '2017-02-10',
        }
        self.invoice_1 = self.env['account.invoice'].create(inv1)
        inv2 = {
            'name': 'i-v-2',
            'type': 'out_invoice',
            'number': '299048',
            'comment': '299048',
            'state': 'draft',
            'date': '2017-02-10',
            'date_invoice': '2017-02-10',
        }
        self.invoice_2 = self.env['account.invoice'].create(inv2)
        fp1 = {
            'fapiao_type': 'customer',
            'tax_type': 'normal',
            'fapiao_number': 1028787,
            'fapiao_date': '2017-02-13',
            'reception_date': '2017-2-14',
            'amount_with_taxes': 10.0,
            'notes': 'SX-19-08',
        }
        self.fapiao_1 = self.env['fapiao'].create(fp1)
        fp2 = {
            'fapiao_type': 'customer',
            'tax_type': 'normal',
            'fapiao_number': 1028787,
            'fapiao_date': '2017-02-13',
            'reception_date': '2017-2-14',
            'amount_with_taxes': 10.0,
            'notes': 'SX-19-08',
        }
        self.fapiao_2 = self.env['fapiao'].create(fp2)

    def test_company_info(self):
        self.assertTrue(
            self.fapiao_tag_1.exists(),
        )
        self.assertTrue(
            self.fapiao_tag_2.exists(),
        )
        self.assertTrue(
            self.invoice_1.exists(),
        )
        self.assertTrue(
            self.invoice_2.exists(),
        )
        self.fapiao_1.invoice_ids.add(self.invoice_1)
        self.fapiao_1.invoice_ids.add(self.invoice_2)
        self.assertTrue(
            self.fapiao_1.exists(),
        )
        self.assertTrue(
            self.fapiao_2.exists(),
        )
