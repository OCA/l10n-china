# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class FapiaoTaxType(models.Model):
    _name = 'fapiao.tax.type'
    _order = 'name'

    name = fields.Char('Name')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tax type must be unique.')
    ]
