from odoo.addons.component.core import Component


class DNSPodRecordDeleter(Component):
    _name = 'dnspod.record.deleter'
    _inherit = 'dns.abstract.deleter'
    _apply_on = 'dnspod.record'
