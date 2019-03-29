import httplib2
import json
from urllib.parse import urlencode

from odoo.addons.component.core import AbstractComponent


class DNSPodAbstractAdapter(AbstractComponent):
    _name = 'dnspod.abstract.adapter'
    _inherit = 'dns.abstract.adapter'

    def _get_login_params(self, domain_id):
        params = {
            'format': 'json',
            'domain_id': domain_id.external_id
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
        return params

    def _send_request(self, uri, params):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json",
            "User-Agent": "DNSPod-Odoo/0.01 (webmaster@my-odoo.com)"
        }
        api_path = self.backend_record.api_path
        conn = httplib2.HTTPSConnectionWithTimeout(api_path)
        conn.request('POST', uri, urlencode(params), headers)
        response = conn.getresponse()
        data = None
        if response.status == 200:
            data = response.read()
            data = json.loads(data.decode('utf-8'))
        conn.close()
        return data
