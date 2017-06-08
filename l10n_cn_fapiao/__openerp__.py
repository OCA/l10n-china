# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Chinese Fapiao Management',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'sequence': 19,
    'summary': 'Chinese Fapiao Management and link with Odoo Invoice',
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.elico-corp.com',
    'depends': ['account'],
    'data': [
        'views/fapiao_view.xml',
        'data/fapiao_tax_type.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/fapiao_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
