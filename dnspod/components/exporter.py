from odoo.addons.component.core import Component


class DNSPodRecordExporter(Component):
    _name = 'dnspod.record.exporter'
    _inherit = 'dns.abstract.exporter'
    _apply_on = 'dnspod.record'

    def _get_external_id(self, response):
        return response['id']
