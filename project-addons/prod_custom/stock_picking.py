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


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    @api.depends('origin')
    def _get_stock_picking_pair(self):
        for stocks in self:
            stocks.stock_picking_pair=""
            stock_pick_pool= self.env['stock.picking'].search([('origin', '=', stocks.origin), ('id', '!=', stocks.id)])
            if stock_pick_pool:
                stocks.stock_picking_pair= stock_pick_pool[0]
            else:
                stock_pick_pool= self.env['stock.picking'].search([('name', '=', stocks.origin), ('id', '!=', stocks.id)])
                if stock_pick_pool:
                    stocks.stock_picking_pair= stock_pick_pool[0]



    stock_picking_pair = fields.Many2one('stock.picking', 'Stock Picking Pair', compute=_get_stock_picking_pair)
    #supplier_ref = fields.Char('Supplier reference')