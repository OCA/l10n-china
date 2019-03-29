# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.addons.component.core import Component


class DNSPodRecordDeleter(Component):
    _name = 'dnspod.record.deleter'
    _inherit = 'dns.abstract.deleter'
    _apply_on = 'dnspod.record'

    def __init__(self, work_context):
        super(DNSPodRecordDeleter, self).__init__(work_context)
        self.record_id = None

    def _before_delete(self, binding):
        self.record_id = binding.odoo_id
        return True

    def _after_delete(self):
        if self.record_id:
            self.record_id.unlink()
        return True
