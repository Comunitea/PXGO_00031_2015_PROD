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


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    is_return_picking = fields.Boolean('Is return picking', compute='_get_is_returned_picking')

    @api.one
    def _get_is_returned_picking(self):
        self.is_return_picking = len([True for x in self.move_lines if x.origin_returned_move_id]) > 0


class stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    move_name = fields.Char('Description', compute='_get_move_name')

    @api.one
    def _get_move_name(self):
        if self.packop_id.linked_move_operation_ids:
            self.move_name = self.packop_id.linked_move_operation_ids[0].move_id.name
