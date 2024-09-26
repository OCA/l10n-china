# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    name = fields.Char(translate=True)
