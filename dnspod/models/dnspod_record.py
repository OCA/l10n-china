# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api
from odoo.addons.component.core import Component


class DNSPodRecord(models.Model):
    _name = 'dnspod.record'
    _inherit = 'dns.binding'
    _inherits = {'dns.record': 'odoo_id'}
    _description = 'DNSPod records'

    @api.model
    def _type_select_version(self):
        res = [('A', 'A'), ('CNAME', 'CNAME'), ('MX', 'MX'),
               ('TXT', 'TXT'), ('NS', 'NS'), ('AAAA', 'AAAA'),
               ('SRV', 'SRV'), ('Visible URL', '显性URL'),
               ('Invisible URL', '隐现URL')]
        return res

    @api.model
    def _line_select_version(self):
        res = [('0', '默认'), ('7=0', '国内'), ('3=0', '国外'), ('10=0', '电信'),
               ('10=1', '联通'), ('10=2', '教育网'), ('10=3', '移动'),
               ('90=0', '百度'), ('90=1', '谷歌'), ('90=2', '有道'),
               ('90=3', '必应'), ('90=4', '搜搜'), ('90=5', '搜狗'),
               ('90=6', '奇虎'), ('80=0', '搜索引擎')]
        return res

    odoo_id = fields.Many2one(comodel_name='dns.record',
                              string='DNS Record',
                              required=True,
                              ondelete='restrict')
    type = fields.Selection(
        selection=_type_select_version,
        string='Record Type'
    )
    line = fields.Selection(
        selection=_line_select_version,
        default='0',
        string='Record Line'
    )
    backend_id = fields.Many2one(
        comodel_name='dns.backend',
        related='domain_id.backend_id'
    )


class DNSPodRecordAdapter(Component):
    _name = 'dnspod.record.adapter'
    _inherit = 'dnspod.abstract.adapter'
    _apply_on = 'dnspod.record'

    def list(self, domain_id, external_id):
        params = self._get_login_params(domain_id)
        params.update(record_id=external_id)
        data = self._send_request('/Record.Info', params)
        if data and data['status']['code'] == '1':
            return data['record']
        return {}

    def list_all(self, domain_id):
        params = self._get_login_params(domain_id)
        data = self._send_request('/Record.List', params)
        if data and data['status']['code'] == '1':
            return [r['id'] for r in data['records']]
        return []

    def create(self, record):
        domain_id = record.domain_id
        params = self._get_login_params(domain_id)
        params.update({
            'sub_domain': record.name,
            'record_type': record.type,
            'record_line_id': record.line,
            'value': record.value,
            'mx': record.mx_priority,
            'ttl': record.ttl
        })
        data = self._send_request('/Record.Create', params)
        if data and data['status']['code'] == '1':
            return data['record']
        return {}

    def write(self, binding):
        domain_id = binding.domain_id
        params = self._get_login_params(domain_id)
        params.update({
            'record_id': binding.external_id,
            'sub_domain': binding.name,
            'record_type': binding.type,
            'record_line_id': binding.line,
            'value': binding.value,
            'mx': binding.mx_priority,
            'ttl': binding.ttl
        })
        self._send_request('/Record.Modify', params)
        return True

    def delete(self, binding):
        domain_id = binding.domain_id
        params = self._get_login_params(domain_id)
        params.update({
            'record_id': binding.external_id,
        })
        self._send_request('/Record.Remove', params)
        return True
