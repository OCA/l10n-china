# -*- coding: utf-8 -*-
# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.connector.unit.synchronizer import Deleter
from openerp.tools.translate import _
from openerp.addons.connector_dns.connector import get_environment
from openerp.addons.connector.queue.job import job


class DNSDeleter(Deleter):
    """ Base deleter for Dnspod """

    def run(self, binding_id, data):
        """ Run the synchronization, delete the record on Dnspod

        :param magento_id: identifier of the record to delete
        """
        result = self.backend_adapter.delete(data)
        if int(result['status']['code']) == 1 \
                or int(result['status']['code']) == 8:
            dns_record = self.env['dns.record'].browse(binding_id)
            dns_record.with_context(connector_no_export=True).write(
                {
                    'record_id': 0
                }
            )
            dns_record.unlink()
        else:
            return _('Record %s delete failed with status code: %s' % (
                binding_id,
                result['status']['code']))
        return _('Record %s deleted on Dnspod') % binding_id


@job
def export_delete_record(session, model_name, backend_id, binding_id, data):
    """ Delete a record on Dnspod """
    env = get_environment(session, model_name, backend_id)
    exporter = env.get_connector_unit(DNSDeleter)
    return exporter.run(binding_id, data)
