# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "l10n_cn_sequence_voucher",
    "version": "9.0.1.0.0",
    "category": "Account",
    "website": "https://www.elico-corp.com",
    "author": "Elico corp",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "l10n_cn_account_voucher",
    ],
    "data": [
        "views/account_journal.xml",
        "views/account_move.xml",
        "data/account_sequence_data.xml",
    ],
}
