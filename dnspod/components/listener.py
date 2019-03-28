# -*- coding: utf-8 -*-
from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if
import uuid


class DNSPodRecordListener(Component):
    _name = 'dnspod.record.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['dnspod.record']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        record.with_delay().sync_dns_records(record.backend_id,
                                             record.domain_id, 'write',
                                             record.external_id)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().sync_dns_records(record.backend_id,
                                             record.domain_id, 'create',
                                             record.id)
