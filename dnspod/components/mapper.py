from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class DNSPodDomainMapper(Component):
    _name = 'dnspod.domain.mapper'
    _inherit = 'dns.abstract.mapper'
    _apply_on = 'dns.domain'

    @mapping
    def compute_state(self, record):
        if record['status']['code'] != '1':
            return {'state': 'exception'}
        else:
            return {'state': 'done'}

    @mapping
    def compute_external_id(self, record):
        if record['status']['code'] != '1':
            return {'external_id': ''}
        else:
            return {'external_id': record['domain']['id']}


class DNSPodRecordMapper(Component):
    _name = 'dnspod.record.mapper'
    _inherit = 'dns.abstract.mapper'
    _apply_on = 'dnspod.record'

    direct = [('id', 'external_id'), ('sub_domain', 'name'),
              ('record_line_id', 'line'), ('record_type', 'type'),
              ('value', 'value'), ('mx', 'mx_priority'),
              ('ttl', 'ttl')]

    @mapping
    def compute_domain(self, record):
        if record.get('domain_id'):
            ext_id = record['domain_id']
            domain_id = self.env['dns.domain'].search(
                [('external_id', '=', ext_id)])
            return {
                'domain_id': domain_id.id,
            }
        return {
            'domain_id': False,
        }
