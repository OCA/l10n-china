# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class FapiaoTag(models.Model):
    _name = 'fapiao.tag'
    _order = 'name'

    name = fields.Char('Name')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tag must be unique.')
    ]
