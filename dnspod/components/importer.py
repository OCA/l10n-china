import httplib2
import json
import logging
from urllib.parse import urlencode

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class DNSPodDomainImporter(Component):
    _name = 'dnspod.domain.importer'
    _inherit = 'dns.abstract.importer'
    _apply_on = 'dns.domain'

    def _get_records(self, signal):
        domain_id = self.domain_id
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json",
            "User-Agent": "DNSPod-Odoo/0.01 (webmaster@my-odoo.com)"
        }
        params = {
            'format': 'json',
            'domain': domain_id.name
        }
        if domain_id.backend_id.token_id and domain_id.backend_id.login_token:
            login_token = '{},{}'.format(
                domain_id.backend_id.token_id,
                domain_id.backend_id.login_token
            )
            params.update(login_token=login_token)
        else:
            params.update(login_email=domain_id.backend_id.login,
                          login_password=domain_id.backend_id.password)
        api_path = self.backend_record.api_path
        conn = httplib2.HTTPSConnectionWithTimeout(api_path)
        conn.request('POST', '/Domain.Info', urlencode(params), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status == 200:
            return json.loads(data.decode('utf-8'))
        else:
            return None

    def _get_binding(self, signal):
        return self.domain_id

    def _update(self, binding, data):
        res = super(DNSPodDomainImporter, self)._update(binding, data)
        self.external_id = binding.external_id
        return res


class DNSPodRecordImporter(Component):
    _name = 'dnspod.record.importer'
    _inherit = 'dns.abstract.importer'
    _apply_on = 'dnspod.record'

    def _get_records(self, signal):
        if signal == 'create':
            return self.backend_adapter.create(self.domain_id,
                                               self.external_id)
        if signal == 'write':
            binding = self._get_binding(signal)
            return self.backend_adapter.write(binding)

        if signal == 'unlink':
            binding = self._get_binding(signal)
            return self.backend_adapter.unlink(binding)

        return self.backend_adapter.send_request(self.domain_id,
                                                 self.external_id)

    def _get_binding(self, signal):
        if signal == 'create':
            return self.model.browse(self.external_id)
        return super(DNSPodRecordImporter, self)._get_binding(signal)

    def _update_data(self, map_record, **kwargs):
        res = super(DNSPodRecordImporter, self)._update_data(map_record,
                                                             **kwargs)
        return {k: v for k, v in res.items() if v}

    def _update(self, binding, data):
        res = super(DNSPodRecordImporter, self)._update(binding, data)
        self.external_id = binding.external_id
        return res

    def _run(self, external_id, signal):
        if signal == 'unlink':
            self.external_id = external_id
            binding = self._get_binding(signal)
            self.backend_adapter.unlink(binding)
        else:
            return super(DNSPodRecordImporter, self)._run(external_id, signal)
