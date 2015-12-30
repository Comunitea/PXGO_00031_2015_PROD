# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
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
##############################################################################
from openerp import models, fields, api, exceptions, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    purchase_ids = fields.Many2many('purchase.order', 'purchase_invoice_rel',
                                    'invoice_id', 'purchase_id',
                                    'Purchase orders', readonly=True)
    sale_ids = fields.Many2many('sale.order', 'sale_order_invoice_rel',
                                'invoice_id', 'order_id', 'Sale orders',
                                readonly=True)
    purchase_str = fields.Char('Purchase orders str', compute='_get_purchase_str')
    sale_str = fields.Char('Sale orders str', compute='_get_sale_str')

    @api.one
    def _get_purchase_str(self):
        self.purchase_str = ', '.join([x.name for x in self.purchase_ids])

    @api.one
    def _get_sale_str(self):
        self.sale_str = ', '.join([x.name for x in self.sale_ids])
