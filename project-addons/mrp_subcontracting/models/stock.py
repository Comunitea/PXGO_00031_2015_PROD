# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@pexego.es>$
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

from openerp import models, api, fields, _, exceptions


class StockWarehouse(models.Model):

    _inherit = "stock.warehouse"

    subcontract_pull_id = fields.Many2one('procurement.rule',
                                          'Subcontract rule')
    subcontract_allow = fields.Boolean('Subcontract allow',
                                       default=True)
    subcontract_type_id = fields.Many2one('stock.picking.type',
                                          'Subcontract type')

    @api.model
    def _get_subcontract_pull_rule(self, warehouse):
        route_obj = self.env['stock.location.route']
        data_obj = self.env['ir.model.data']
        try:
            subcontract_route_id = data_obj.\
                get_object_reference('mrp_subcontracting',
                                     'route_wh0_subcontract')[1]
        except:
            subcontract_route_id = route_obj.search([('name', 'like',
                                                      _('Subcontract'))])
            subcontract_route_id = subcontract_route_id and \
                subcontract_route_id[0] or False
        if not subcontract_route_id:
            raise exceptions.Warning(_('Can\'t find any generic Subcontract '
                                       'route.'))

        return {
            'name': self._format_routename(warehouse, _(' Subcontract')),
            'location_id': warehouse.lot_stock_id.id,
            'route_id': subcontract_route_id,
            'action': 'buy',
            'picking_type_id': warehouse.subcontract_type_id.id,
            'warehouse_id': warehouse.id,
        }

    @api.multi
    def create_routes(self, warehouse):
        pull_obj = self.env['procurement.rule']
        res = super(StockWarehouse, self).create_routes(warehouse)
        if warehouse.subcontract_allow:
            subcontract_pull_vals = self._get_subcontract_pull_rule(warehouse)
            subcontract_pull_id = pull_obj.create(subcontract_pull_vals)
            res['subcontract_pull_id'] = subcontract_pull_id.id
        return res

    @api.multi
    def write(self, vals):
        pull_obj = self.env['procurement.rule']
        if 'subcontract_allow' in vals:
            if vals.get("subcontract_allow"):
                for warehouse in self:
                    if not warehouse.subcontract_pull_id:
                        subcontract_pull_vals = self.\
                            _get_subcontract_pull_rule(warehouse)
                        subcontarct_pull_id = pull_obj.\
                            create(subcontract_pull_vals)
                        vals['subcontract_pull_id'] = subcontarct_pull_id.id
                    if not warehouse.subcontract_type_id:
                        data_obj = self.env['ir.model.data']
                        subcontract_pick_type_id = data_obj.\
                            get_object_reference('mrp_subcontracting',
                                                 'picking_type_subcontract')[1]
                        vals['subcontract_type_id'] = subcontract_pick_type_id
            else:
                for warehouse in self:
                    if warehouse.subcontract_pull_id:
                        warehouse.subcontract_pull_id.unlink()
        return super(StockWarehouse, self).write(vals)

    @api.model
    def get_all_routes_for_wh(self, warehouse):
        all_routes = super(StockWarehouse, self).\
            get_all_routes_for_wh(warehouse)
        if (warehouse.subcontract_allow and
                warehouse.subcontract_pull_id and
                warehouse.subcontract_pull_id.route_id):
            all_routes += [warehouse.subcontract_pull_id.route_id.id]
        return all_routes

    @api.model
    def _handle_renaming(self, warehouse, name, code):
        res = super(StockWarehouse, self)._handle_renaming(warehouse, name,
                                                           code)
        # change the subcontract pull rule name
        if warehouse.subcontract_pull_id:
            warehouse.subcontract_pull_id.\
                write({'name': warehouse.subcontract_pull_id.
                       name.replace(warehouse.name, name, 1)})
        return res


class StockPickingType(models.Model):

    _inherit = "stock.picking.type"

    force_purchase_dest = fields.Boolean('Force purchase dest.',
                                         help="Forces dest. location on "
                                              "purchase orders with this type "
                                         )
