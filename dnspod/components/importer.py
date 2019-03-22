# -*- coding: utf-8 -*-
from odoo.addons.component.core import Component


class DNSImporter(Component):
    _name = 'dns.importer'
    _inherit = 'dns.abstract.importer'

    def _before_import(self):
        print('import start')

    def _after_import(self):
        print('import done')

    def _send_request(self, signal):
        print('hello world')
