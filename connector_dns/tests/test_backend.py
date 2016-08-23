# -*- coding: utf-8 -*-
# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import openerp.tests.common as common
from openerp.addons.connector.backend import Backend


class TestBackend(common.TransactionCase):
    """
    test generic Backend
    """

    def setUp(self):
        super(TestBackend, self).setUp()
        self.service = "dns"
        self.version = "1.7"

    def tearDown(self):
        super(TestBackend, self).tearDown()

    def test_dnspod(self):
        dnspod = Backend(self.service)
        self.assertEqual(dnspod.service, self.service)

    def test_child_dnspod(self):
        dnspod = Backend(self.service)
        child_dnspod = Backend(parent=dnspod, version=self.service)
        self.assertEqual(child_dnspod.service, dnspod.service)
