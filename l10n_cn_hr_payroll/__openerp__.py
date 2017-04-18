# -*- coding: utf-8 -*-
# © 2016 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Chinese - Payroll',
    'category': 'Localization',
    'version': '9.0.2.0.0',
    'website': 'https://www.elico-corp.com',
    'author': "Elico Corp, Odoo Community Association (OCA)",
    'depends': ['hr_payroll'],
    'demo': [
    ],
    'data':
    [
        'views/l10n_cn_hr_payroll_view.xml',
        'views/report_payslip.xml',
        'data/leave_type_data.xml',
        'data/salary_rule_category.xml',
        'data/salary_rule_basic.xml',
        'data/salary_rule_sz1.xml',
        'data/salary_rule_sz2.xml',
        'data/salary_rule_sz3.xml',
        'data/salary_rule_sz4.xml',
        'data/salary_rule_sh1.xml',
        'data/salary_rule_sh2.xml',
        'data/salary_rule_sh3.xml',
        'data/salary_rule_sh4.xml',
        'data/salary_rule_nj1.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
