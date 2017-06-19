# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from openerp.tests import common
from psycopg2 import IntegrityError
import openerp.tools


class TestFapiao(common.TransactionCase):
    def setUp(self):
        super(TestFapiao, self).setUp()
        self.fapiao_tag_model = self.env['fapiao.tag']
        self.fapiao_tax_type_model = self.env['fapiao.tax.type']
        self.res_partner_model = self.env['res.partner']
        self.account_invoice_model = self.env['account.invoice']

        self.partner_agrolait_id = self.env.ref("base.res_partner_2")
        self.currency_swiss_id = self.env.ref("base.CHF")
        self.account_rcv_id = self.env.ref("account.a_recv")

    def test_00_data_creation(self):
        fapiao_tag_1 = self.fapiao_tag_model.create({
            'name': 'Fapiao Tag 1',
        })
        fapiao_tag_2 = self.fapiao_tag_model.create({
            'name': 'Fapiao Tag 2',
        })
        fapiao_tax_type_1 = self.fapiao_tax_type_model.create({
            'name': 'Fapiao Tax Type 1'
        })
        fapiao_tax_type_2 = self.fapiao_tax_type_model.create({
            'name': 'Fapiao Tax Type 2'
        })
        fapiao_1 = self.env['fapiao'].create({
            'fapiao_type': 'customer',
            'tax_type': fapiao_tax_type_1.id,
            'fapiao_number': 1028787,
            'fapiao_date': '2017-02-13',
            'reception_date': '2017-2-14',
            'amount_with_taxes': 10.0,
            'notes': 'SX-19-08',
        })
        fapiao_2 = self.env['fapiao'].create({
            'fapiao_type': 'supplier',
            'tax_type': fapiao_tax_type_2.id,
            'fapiao_number': 1028788,
            'fapiao_date': '2017-02-13',
            'reception_date': '2017-2-14',
            'amount_with_taxes': 10.0,
            'notes': 'SX-19-08',
        })
        invoice_1 = self.account_invoice_model.create({
            'name': 'invoice in',
            'reference_type': 'none',
            'currency_id': self.currency_swiss_id.id,
            'account_id': self.account_rcv_id.id,
            'type': 'in_invoice',
            'date_invoice': time.strftime('%Y') + '-07-01',
            'partner_id': self.partner_agrolait_id.id,
        })
        invoice_2 = self.account_invoice_model.create({
            'name': 'invoice out',
            'reference_type': 'none',
            'currency_id': self.currency_swiss_id.id,
            'account_id': self.account_rcv_id.id,
            'type': 'out_invoice',
            'date_invoice': time.strftime('%Y') + '-07-01',
            'partner_id': self.partner_agrolait_id.id,
        })

        # def test_01_company_info(self):
        self.assertTrue(fapiao_tag_1.exists())
        self.assertTrue(fapiao_tag_2.exists())
        self.assertTrue(fapiao_tax_type_1.exists())
        self.assertTrue(fapiao_tax_type_2.exists())
        self.assertTrue(fapiao_1.exists())
        self.assertTrue(fapiao_2.exists())
        self.assertTrue(invoice_1.exists())
        self.assertTrue(invoice_2.exists())

        # test fapiao with tag
        fapiao_1.tag_ids += fapiao_tag_1
        self.assertEqual(len(fapiao_1.tag_ids), 1)

        for fapiao_tag in fapiao_1.tag_ids:
            self.assertTrue(fapiao_tag.exists())

        # test fapiao with tag
        fapiao_2.tag_ids += fapiao_tag_1
        fapiao_2.tag_ids += fapiao_tag_2
        self.assertEqual(len(fapiao_2.tag_ids), 2)

        for fapiao_tag in fapiao_2.tag_ids:
            self.assertTrue(fapiao_tag.exists())

        # test invoice with fapiao
        invoice_1.fapiao_ids += fapiao_1
        self.assertEqual(len(invoice_1.fapiao_ids), 1)

        for fapiao in invoice_1.fapiao_ids:
            self.assertTrue(fapiao.exists())

        # test invoice with fapiao
        invoice_2.fapiao_ids += fapiao_1
        invoice_2.fapiao_ids += fapiao_2
        self.assertEqual(len(invoice_2.fapiao_ids), 2)

        for fapiao in invoice_1.fapiao_ids:
            self.assertTrue(fapiao.exists())

    @openerp.tools.mute_logger('openerp.sql_db')
    def test_01_tag_constraint(self):
        self.fapiao_tag_model.create({
            'name': 'Fapiao Tag',
        })
        with self.assertRaises(IntegrityError):
            self.fapiao_tag_model.create({
                'name': 'Fapiao Tag',
            })

    @openerp.tools.mute_logger('openerp.sql_db')
    def test_02_tax_type_constraint(self):
        self.fapiao_tax_type_model.create({
            'name': 'Fapiao Tax Type'
        })
        with self.assertRaises(IntegrityError):
            self.fapiao_tax_type_model.create({
                'name': 'Fapiao Tax Type'
            })

    def test_03_fapiao_default_value(self):
        self.env['fapiao'].create({
            'fapiao_number': 1028787,
            'fapiao_date': '2017-02-13',
            'reception_date': '2017-2-14',
            'amount_with_taxes': 10.0,
            'notes': 'SX-19-08',
        })
