# © 2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'DNS Pod',
    'category': 'connector',
    'version': '12.0.1.0.0',
    'depends': [
        'dns',
    ],
    'external_dependencies': {
        'python': ['httplib2'],
    },
    'data': [
        'views/dns_backend_views.xml',
        'views/dnspod_domain_views.xml',
        'views/dnspod_record_views.xml',
    ],
}
