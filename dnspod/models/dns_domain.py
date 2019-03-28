# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api, _


class DNSDomain(models.Model):
    _inherit = 'dns.domain'

    @api.multi
    def action_connect(self):
        for domain in self:
            domain.sync_dns_domains(domain.backend_id, domain, None,
                                    domain.external_id)

    @api.multi
    def action_subdomains(self):
        for domain in self:
            self.env['dnspod.record'].sync_dns_records(domain.backend_id,
                                                       domain)
