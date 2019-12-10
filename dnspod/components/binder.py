# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.addons.component.core import Component


class DNSBinder(Component):
    _inherit = 'dns.binder'
    _apply_on = ['dns.domain', 'dnspod.record']
