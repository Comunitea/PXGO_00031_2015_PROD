# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Kiko Sánchez <kiko@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
##############################################################################

from openerp import models, fields, api, exceptions


class account_invoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):

        user_id = self.env['res.partner'].search(
            [('id', '=', partner_id)]).user_id or self.env.user

        res = super(account_invoice,
                    self).onchange_partner_id(type,
                                              partner_id,
                                              date_invoice=date_invoice,
                                              payment_term=payment_term,
                                              partner_bank_id=partner_bank_id,
                                              company_id=company_id)

        if partner_id:
            res['value']['user_id'] = user_id
        return res
