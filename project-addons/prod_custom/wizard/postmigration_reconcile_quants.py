# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2013 QUIVAL, S.A. All Rights Reserved
#    $Pedro Gómez Campos$ <pegomez@elnogal.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp import models, api

class postmigration_reconcile_quants(models.TransientModel):
    _name = 'postmigration.reconcile.quants'

    @api.multi
    def reconcile_quants(self):
        t_move = self.env["stock.move"]
        stock_warehouses = []

        for wh in self.env['stock.warehouse'].search([]):
            if wh.wh_input_stock_loc_id:
                stock_warehouses.append(wh.wh_input_stock_loc_id.id)
        domain = [('location_id.usage', '=', 'internal'),
                  ('qty', '<', 0)
        ]
        quants = self.env['stock.quant'].search(domain)
        for product in quants.mapped('product_id'):
            domain = [('location_id.usage', '=', 'internal'),
                      ('qty', '>', 0), ('product_id', '=', product.id)
            ]
            product_quants = self.env['stock.quant'].search(domain)
            for quant in product_quants:
                self.env['stock.quant']._quant_reconcile_negative(quant, False)
        return True
