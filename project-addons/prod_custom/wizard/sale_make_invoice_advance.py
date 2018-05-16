# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def _prepare_advance_invoice_vals(self):
        result = super(SaleAdvancePaymentInv, self)._prepare_advance_invoice_vals()
        for res in result:
            sale = self.env['sale.order'].browse(res[0])
            res[1]['payment_mode_id'] = sale.payment_mode_id.id
            res[1]['partner_bank_id'] = sale.payment_mode_id.bank_id.id
        return result
