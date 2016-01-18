# -*- coding: utf-8 -*-
# © 2016 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


@common.at_install(False)
@common.post_install(True)
class PayrollTestCase(common.TransactionCase):
    def setUp(self):
        super(PayrollTestCase, self).setUp()
        self.ModelDataObj = self.env['ir.model.data']
        self.StructA = self.ModelDataObj.xmlid_to_res_id(
            'l10n_cn_hr_payroll.hr_payroll_salary_structure_sz1')
        self.EmployeeObj = self.env['hr.employee']
        self.EmployeeA = self.EmployeeObj.create({
            'name': 'Xie Xiaopeng'})
        self.ContractObj = self.env['hr.contract']
        contract_val = {
            'name': 'XieXiaopeng2016',
            'employee_id': self.EmployeeA.id,
            'wage': 20000,
            'struct_id': self.StructA,
            'pit_base_amount': 10000,
            'social_insurance_amount': 5000,

        }
        self.ContractA = self.ContractObj.create(contract_val)

        self.PayslipObj = self.env['hr.payslip']
        self.PayslipA = self.PayslipObj.create({
            'employee_id': self.EmployeeA.id,
        })
        self.PayslipA.compute_sheet(self.PayslipA.id)

        for line in self.PayslipA.line_ids:
            if line.name == 'BASIC':
                self.assertEqual(line.amount, self.ContractA.wage)
            if line.name == 'SZHKPP':
                self.assertEqual(line.amount, self.ContractA.wage)
