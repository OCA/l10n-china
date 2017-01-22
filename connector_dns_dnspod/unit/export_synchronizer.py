# -*- coding: utf-8 -*-
# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.connector_dns.unit.export_synchronizer \
    import DNSBaseExporter
from openerp.addons.connector_dns.connector import get_environment
from openerp.tools.translate import _
from openerp.addons.connector.queue.job import job


class DNSExporter(DNSBaseExporter):

    """ A common flow for the exports to DNS """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(DNSExporter, self).__init__(environment)
        self.binding_record = None

    def _run(self, fields=None, method='create'):
        """ Flow of the synchronization, implemented in inherited classes"""
        assert self.binding_id
        assert self.binding_record
        record = self.mapper.map_record(self.binding_record).values()
        if not record:
            return _('Nothing to export.')
        if method == 'create':
            result = self._create(record)
            if int(result['status']['code']) == 1:
                self.external_id = result['id']
                self.binding_record.with_context(connector_no_export=True).write(
                    {
                        'record_id': result['id']
                    }
                )
                return _('Record successfully exported in DNSPod.')
            else:
                return _('Record export failed with status code: %s' % (
                    result['status']['code']))
        elif method == 'write':
            result = self._update(record)
            if int(result['status']['code']) == 1:
                self.external_id = result['id']
                self.binding_record.with_context(connector_no_export=True).write(
                    {
                        'record_id': result['id']
                    }
                )
                return _('Record successfully exported in DNSPod.')
            else:
                return _('Record export failed with status code: %s' % (
                    result['status']['code']))

    def _create(self, data):
        """ Create the DNS record """
        return self.backend_adapter.create(data)

    def _unlink(self, data):
        """ Create the DNS record """
        return self.backend_adapter.delete(data)

    def _update(self, data):
        """ Update an DNS record """
        return self.backend_adapter.write(data)


@job
def export_record(
        session, model_name, binding_id, fields=None, method='create'):
    """ Export a record on DNS """
    record = session.browse(model_name, binding_id)
    env = get_environment(session, model_name, record.backend_id.id)
    exporter = env.get_connector_unit(DNSExporter)
    result = exporter.run(binding_id, fields=fields, method=method)
    return result
