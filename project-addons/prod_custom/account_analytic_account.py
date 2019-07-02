# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    invoice_name = fields.Char('Invoice reference')

    @api.model
    def _prepare_invoice_data(self, contract):
        invoice_vals = super(AccountAnalyticAccount, self).\
            _prepare_invoice_data(contract)
        if contract.invoice_name:
            invoice_vals['name'] = contract.invoice_name
        return invoice_vals
