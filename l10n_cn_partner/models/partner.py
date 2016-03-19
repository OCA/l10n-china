# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Partner(models.Model):
    """Add a contact Address type."""

    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[
        ("residence_address", "Residence Address"), ("huji2", "huji2")
    ])
