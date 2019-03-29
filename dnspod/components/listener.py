from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class DNSPodRecordListener(Component):
    _name = 'dnspod.record.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['dnspod.record']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        record.with_delay().export_dns_records(record.backend_id, record)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().export_dns_records(record.backend_id, record)

    def on_record_unlink(self, record):
        record.delete_dns_records(record.backend_id, record)
