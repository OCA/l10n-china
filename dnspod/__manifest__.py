{
    'name': 'DNS Pod',
    'category': 'connector',
    'version': '12.0.1.0.0',
    'depends': [
        'dns',
    ],
    'data': [
        'views/dns_backend_views.xml',
        'views/dnspod_domain_views.xml',
        'views/dnspod_record_views.xml',
    ],
}
