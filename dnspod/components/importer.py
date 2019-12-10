# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.addons.component.core import Component


class DNSPodDomainImporter(Component):
    _name = 'dnspod.domain.importer'
    _inherit = 'dns.abstract.importer'
    _apply_on = 'dns.domain'

    def _get_records(self):
        return self.backend_adapter.search(self.domain_id)

    def _get_binding(self):
        return self.domain_id

    def _update(self, binding, data):
        res = super(DNSPodDomainImporter, self)._update(binding, data)
        self.external_id = binding.external_id
        return res


class DNSPodRecordImporter(Component):
    _name = 'dnspod.record.importer'
    _inherit = 'dns.abstract.importer'
    _apply_on = 'dnspod.record'

    def _get_records(self):
        return self.backend_adapter.search(self.domain_id, self.external_id)

    def _update_data(self, map_record, **kwargs):
        res = super(DNSPodRecordImporter, self)._update_data(map_record,
                                                             **kwargs)
        return {k: v for k, v in res.items() if v}

    def _update(self, binding, data):
        res = super(DNSPodRecordImporter, self)._update(binding, data)
        self.external_id = binding.external_id
        return res
