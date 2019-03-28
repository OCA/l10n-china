# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api


class DNSBackend(models.Model):
    _inherit = 'dns.backend'

    token_id = fields.Char('Token ID')
    login_token = fields.Char('Login Token')
