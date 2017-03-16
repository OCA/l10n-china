# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Chinese Fapiao Management',
    'version': '8.0.0.0.1',
    'category': 'Accounting',
    'sequence': 19,
    'summary': 'Chinese Fapiao Management and link with OpenERP Invoice',
    'description': """

* "Fapiao" is an official invoice in China, printed in a separate official software.
* This module allows the users to manage all emitted and received "fapiao"  as object in OpenERP. It has no impact on accounting books and doesnot (yet) integrate with external official software. It adds new submenu called Fapiao under the menu Accounting.

The procedure to follow for the fapiao management is as below:
* Step 1: A fapiao is received or emitted
* Step 2: The document can be scanned as image
* Step 3: A new fapiao is created in OpenERP
* Step 4: The scanned document is uploaded to the newly created object as attachment.
* Step 5: Fapiao allocation to invoice: Fapiao and OpenERP invoices can be linked to each other
    """,
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.elico-corp.com',
    'images': [],
    'depends': ['account'],
    'data': [
        'fapiao_view.xml',
    ],
    'test': [
    ],
    'demo': [
        'fapiao_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
