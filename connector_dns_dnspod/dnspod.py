# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2015 Elico Corp (<http://www.elico-corp.com>)
#    Authors: Liu Lixia, Augustin Cisterne-Kaas
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import httplib
import json
import logging
import urllib

from openerp import _
from openerp import fields
from openerp import models, api
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.unit.mapper import (
    mapping, ExportMapper)
from .backend import dnspod
from .unit.backend_adapter import DNSPodAdapter
from .unit.delete_synchronizer import export_delete_record, DNSDeleter
from .unit.export_synchronizer import DNSExporter

_logger = logging.getLogger(__name__)


class DNSPodBackend(models.Model):
    _inherit = 'dns.backend'

    def _select_version(self):
        """return version selection"""
        res = []
        res.append(('dnspod', 'dnspod'))
        return res

    @api.multi
    def params(self):
        return {'format': 'json', 'login_email': self.login,
                'login_password': self.password}

    def request(self, action, params, method='POST'):
        """send request to 'dnsapi.cn'"""
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json"
        }
        conn = httplib.HTTPSConnection("dnsapi.cn")
        conn.request(method, '/' + action, urllib.urlencode(params), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status == 200:
            return data
        else:
            return None

    @api.one
    def button_connect(self):
        params = self.params()
        data = self.request('Domain.List', params)
        data = json.loads(data)
        if int(data['status']['code']) != -1:
            self.state = 'done'
        else:
            self.state = 'exception'

    @api.one
    def button_set_draft(self):
        self.state = 'draft'


class DNSPodDomain(models.Model):
    _inherit = 'dns.domain'

    @api.one
    def button_get_sub_domains(self):
        """ Create a job which import all the bindings of a record."""
        session = ConnectorSession(self._cr, self._uid, context=self._context)
        if session.context.get('connector_no_export'):
            return
        data = {}
        data['format'] = 'json'
        data['login_email'] = self.backend_id.login
        data['login_password'] = self.backend_id.password
        data['domain_id'] = self.dns_id
        import_record.delay(session, self.id, data)


@job
def import_record(session, dns_domain_id, data):
    dns_record_model = session.env['dns.record']
    dns_domain_model = session.env['dns.domain']
    dns_domain = dns_domain_model.browse(dns_domain_id)
    if not dns_domain:
        return _(u'Nothing to do because the record has been deleted.')

    try:
        result = dns_domain.backend_id.request('Record.List', data, method='POST')

        result_json = json.loads(result)
        if result_json['status']['code'] == '1':
            for record in result_json['records']:
                dns_record_id = dns_record_model.search([('name', '=', record['name'])])
                if record['type'] == 'NS':
                    continue
                if dns_record_id:
                    dns_record_id[0]\
                        .with_context(connector_no_export=True)\
                        .write({
                            'record_id': record['id'],
                            'domain_id': dns_domain.id,
                            'type': record['type'],
                            'line': record['line'],
                            'value': record['value'],
                            'mx_priority': record['mx'],
                            'ttl': record['ttl'],
                            'backend_id': dns_domain.backend_id.id,
                        })
                else:
                    dns_record_model \
                        .with_context(connector_no_export=True)\
                        .create({
                            'record_id': record['id'],
                            'name': record['name'],
                            'domain_id': dns_domain.id,
                            'type': record['type'],
                            'line': record['line'],
                            'value': record['value'],
                            'mx_priority': record['mx'],
                            'ttl': record['ttl'],
                            'backend_id': dns_domain.backend_id.id,
                        })
        else:
            raise result
    except:
        raise


class DNSPodRecord(models.Model):
    _inherit = 'dns.record'

    record_id = fields.Integer(string="Record id on dnspod.cn")

    def _type_select_version(self):
        res = [('A', 'A'), ('CNAME', 'CNAME'), ('MX', 'MX'),
               ('TXT', 'TXT'), ('NS', 'NS'), ('AAAA', 'AAAA'),
               ('SRV', 'SRV'), ('Visibile URL', '显性URL'),
               ('Invisible URL', '隐现URL')]
        return res

    def _line_select_version(self):
        res = [(u'\u9ed8\u8ba4', '默认'), ('B', '电信'), ('C', '联通'),
               ('D', '教育网'), ('E', '百度'), ('F', '搜索引擎')]
        return res

    @api.multi
    def unlink(self):
        for dns_record in self:
            if dns_record.record_id == 0:
                super(DNSPodRecord, dns_record).unlink()
            else:
                dns_record.delete_record()

    @api.model
    def delete_record(self):
        """ Create a job which delete all the bindings of a record. """
        session = ConnectorSession(self._cr, self._uid, context=self._context)
        data = {}
        data['format'] = 'json'
        data['login_email'] = self.backend_id.login
        data['login_password'] = self.backend_id.password
        data['domain_id'] = self.domain_id.dns_id
        data['record_id'] = self.record_id
        export_delete_record.delay(session, self._model._name,
                                   self.backend_id.id, self.id, data=data)


@dnspod
class DNSRecordDeleter(DNSDeleter):
    _model_name = ['dns.record']


@dnspod
class DNSRecordExport(DNSExporter):
    _model_name = ['dns.record']


@dnspod
class DNSRecordAdapter(DNSPodAdapter):
    _model_name = 'dns.record'
    _dns_model = 'Record'


@dnspod
class DNSRecordExportMapper(ExportMapper):
    _model_name = 'dns.record'
    direct = [('name', 'record')]

    @mapping
    def default(self, record):
        result = {
            'format': 'json',
            'login_email': record.domain_id.backend_id.login,
            'login_password': record.domain_id.backend_id.password,
            'record_id': record.record_id,
            'domain_id': record.domain_id.dns_id,
            'sub_domain': record.name,
            'record_type': record.type,
            'record_line': record.line.encode('utf-8'),
            'value': record.value,
            'mx': record.mx_priority,
            'ttl': record.ttl,
        }
        return result


@dnspod
class DNSDomainExport(DNSExporter):
    _model_name = ['dns.domain']


@dnspod
class DNSDomainAdapter(DNSPodAdapter):
    _model_name = 'dns.domain'
    _dns_model = 'Domain'


@dnspod
class DNSDomainExportMapper(ExportMapper):
    _model_name = 'dns.domain'
    direct = [('name', 'domain')]

    @mapping
    def default(self, record):
        return {
            'format': 'json',
            'login_email': record.backend_id.login,
            'login_password': record.backend_id.password
        }
