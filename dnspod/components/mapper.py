# -*- coding: utf-8 -*-
from odoo.addons.component.core import Component


class DNSRecordMapper(Component):
    _name = 'dns.record.mapper'
    _inherit = 'dns.abstract.mapper'
    _usage = 'import.mapper'
