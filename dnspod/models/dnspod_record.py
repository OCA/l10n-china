# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import httplib2
import json
from urllib.parse import urlencode

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
        string='Record Line'
    )
    backend_id = fields.Many2one(
        comodel_name='dns.backend',
        related='domain_id.backend_id'
    )


class DNSPodRecordAdapter(Component):
    _name = 'dnspod.record.adapter'
    _inherit = 'dns.abstract.adapter'
    _apply_on = 'dnspod.record'

    _headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
        "User-Agent": "DNSPod-Odoo/0.01 (webmaster@my-odoo.com)"
    }

    def search(self, domain_id):
        params = {
            'format': 'json',
            'domain_id': domain_id.external_id
        }
        if domain_id.backend_id.token_id and domain_id.backend_id.login_token:
            login_token = '{},{}'.format(
                domain_id.backend_id.token_id,
                domain_id.backend_id.login_token
            )
            params.update(login_token=login_token)
        else:
            params.update(login_email=domain_id.backend_id.login,
                          login_password=domain_id.backend_id.password)
        api_path = self.backend_record.api_path
        conn = httplib2.HTTPSConnectionWithTimeout(api_path)
        conn.request('POST', '/Record.List',
                     urlencode(params), self._headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status == 200:
            res = json.loads(data.decode('utf-8'))
            if res['status']['code'] == '1':
                return [r['id'] for r in res['records']]
        return []

    def send_request(self, domain_id, external_id):
        params = {
            'format': 'json',
            'domain_id': domain_id.external_id,
            'record_id': external_id
        }
        if domain_id.backend_id.token_id and domain_id.backend_id.login_token:
            login_token = '{},{}'.format(
                domain_id.backend_id.token_id,
                domain_id.backend_id.login_token
            )
            params.update(login_token=login_token)
        else:
            params.update(login_email=domain_id.backend_id.login,
                          login_password=domain_id.backend_id.password)
        api_path = self.backend_record.api_path
        conn = httplib2.HTTPSConnectionWithTimeout(api_path)
        conn.request('POST', '/Record.Info',
                     urlencode(params), self._headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status == 200:
            res = json.loads(data.decode('utf-8'))
            if res['status']['code'] == '1':
                return res['record']
        return None
