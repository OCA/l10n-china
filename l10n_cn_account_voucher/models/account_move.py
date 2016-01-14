# -*- coding: utf-8 -*-
# © 2016 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from math import ceil


class AccountMove(models.Model):
    _inherit = 'account.move'

    proof = fields.Integer('Attachment Count', required=False, default=1)

    def _paginate(self, items, max_per_page=5):
        """
        The paging function
        items is to page entry
        max_per_page Set the number of each page
        return：Number of pages
        """
        count = len(items)
        return int(ceil(float(count) / max_per_page))

    @api.multi
    def _get_account_name(self, id):
        account_name = self.env['account.account'].browse(id).name_get()[0]
        # Account move print use Account here:
        return account_name[1]

    @api.model
    def _get_account_partner(self, id, name):
        value = 'account.account,' + str(id)
        partner_prop_acc = self.env['ir.property'].search(
            [('value_reference', '=', value)])
        if partner_prop_acc:
            return name
        else:
            return False

    def _get_exchange_rate(self, line):
        '''
        Exchange rate: Debit or Credit / currency ammount
        Why not get it from currency code + date ?
        '''
        exchange_rate = False
        if line.amount_currency:
            if line.debit > 0:
                exchange_rate = line.debit / line.amount_currency
            if line.credit > 0:
                exchange_rate = line.credit / (-1 * line.amount_currency)
        return round(exchange_rate, 6)

    def _get_unit_price(self, line):
        '''
        Unit price：Debit or Credit / Quantity
        '''
        unit_price = False
        if line.quantity:
            if line.debit > 0:
                unit_price = line.debit / line.quantity
            if line.credit > 0:
                unit_price = line.credit / line.quantity
        return unit_price

    def _rmb_format(self, value):
        """
        Separate numerical according to the figures
        """
        rounding = self.env['res.currency'].browse(
            self.company_id.currency_id.id).rounding

        if value < rounding:
            # if value is 0，return 0.00
            return (['' for i in range(12)] + list((
                '%0.2f' % 0).replace('.', '')))[-12:]
        # change num to string, remove The decimal point
        # get 12 itmes and return
        return (['' for i in range(12)] + list((
            '%0.2f' % value).replace('.', '')))[-12:]

    def _rmb_upper(self, value):
        """
        in capital letters
        from：http://topic.csdn.net/u/20091129/20/b778a93d-9f8f-4829-9297-d05b08a23f80.html
        To float value is returned, unicode string
        """
        rmbmap = [u"零", u"壹", u"贰", u"叁", u"肆", u"伍", u"陆", u"柒", u"捌", u"玖"]
        unit = [u"分", u"角", u"元", u"拾", u"佰", u"仟", u"万", u"拾", u"佰", u"仟",
                u"亿", u"拾", u"佰", u"仟", u"万", u"拾", u"佰", u"仟", u"兆"]
        nums = map(int, list(str('%0.2f' % value).replace('.', '')))
        words = []
        # Tag 0 times in a row, to remove a swastika,
        # insert zero word or timely
        zflag = 0
        start = len(nums) - 3
        # Make I corresponds to the actual figures,
        # negative for the corner points
        for i in range(start, -3, -1):
            if 0 != nums[start - i] or len(words) == 0:
                if zflag:
                    words.append(rmbmap[0])
                    zflag = 0
                words.append(rmbmap[nums[start - i]])
                words.append(unit[i + 2])
            # Control 'ten thousand/yuan'
            elif 0 == i or (0 == i % 4 and zflag < 3):
                words.append(unit[i + 2])
                zflag = 0
            else:
                zflag += 1
        # At the end of the 'points' to fill the whole word
        if words[-1] != unit[0]:
            words.append(u"整")
        return ''.join(words)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    currency_rate = fields.Float(
        'Currency Rate', digits=(10, 6), compute='_compute_currency_rate')

    @api.depends('credit', 'debit', 'amount_currency')
    def _compute_currency_rate(self):
        for record in self:
            if record.currency_id:
                if record.amount_currency:
                    record.currency_rate = abs(
                        (record.debit
                            or record.credit) / record.amount_currency)
                else:
                    record.currency_rate = False
