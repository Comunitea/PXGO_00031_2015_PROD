# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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
from lxml import etree


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    supplier_ref = fields.Char('Supplier reference')
    stock_picking_pair = fields.Many2one('stock.picking', 'Stock Picking Pair',
                                         compute='_get_stock_picking_pair')
    partner_id = fields.Many2one(states={'done': [('readonly', False)],
                                         'cancel': [('readonly', True)]})

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(StockPicking, self)._get_invoice_vals(key, inv_type,
                                                          journal_id, move)
        res['supplier_picking_ref'] = move.picking_id.supplier_ref
        return res

    @api.multi
    @api.depends('origin')
    def _get_stock_picking_pair(self):
        for stocks in self:
            if stocks.id and stocks.origin:
                stocks.stock_picking_pair = ""
                stock_pick_pool = self.env['stock.picking'].search(
                    [('origin', '=', stocks.origin), ('id', '!=', stocks.id)])
                if stock_pick_pool:
                    stocks.stock_picking_pair = stock_pick_pool[0]
                else:
                    stock_pick_pool = self.env['stock.picking'].search(
                        [('name', '=', stocks.origin),
                         ('id', '!=', stocks.id)])
                    if stock_pick_pool:
                        stocks.stock_picking_pair = stock_pick_pool[0]
