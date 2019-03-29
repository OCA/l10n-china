# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.addons.component.core import Component


class DNSPodRecordDeleter(Component):
    _name = 'dnspod.record.deleter'
    _inherit = 'dns.abstract.deleter'
    _apply_on = 'dnspod.record'
