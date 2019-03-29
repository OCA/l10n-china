# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import json

from odoo import models, fields, api, _
from odoo.addons.component.core import Component


class DNSDomain(models.Model):
    _inherit = 'dns.domain'

    @api.multi
    def action_connect(self):
        for domain in self:
            domain.import_dns_domains(domain.backend_id, domain)

    @api.multi
    def action_subdomains(self):
        for domain in self:
            self.env['dnspod.record'].import_dns_records(domain.backend_id,
                                                         domain)


class DNSDomainAdapter(Component):
    _name = 'dns.domain.adapter'
    _inherit = 'dnspod.abstract.adapter'
    _apply_on = 'dns.domain'

    def _get_login_params(self, domain_id):
        params = super(DNSDomainAdapter, self)._get_login_params(domain_id)
        params.pop('domain_id', False)
        params.update(domain=domain_id.name)
        return params

    def list(self, domain_id):
        params = self._get_login_params(domain_id)
        data = self._send_request('/Domain.Info', params)
        if data and data['status']['code'] == '1':
            return data
        return {}

    def list_all(self, domain_id):
        return [domain_id.id]
