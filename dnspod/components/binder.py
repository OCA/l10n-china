from odoo.addons.component.core import Component


class DNSBinder(Component):
    _inherit = 'dns.binder'
    _apply_on = ['dns.domain', 'dnspod.record']
