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

    def _get_records(self, signal):
        return self.backend_adapter.send_request(self.domain_id,
                                                 self.external_id)
