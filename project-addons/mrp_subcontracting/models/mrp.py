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

from openerp import models, api, fields
from openerp.osv import osv, orm


class MrpProduction(models.Model):

    _inherit = "mrp.production"

    @api.model
    def action_produce(self, production_id, production_qty, production_mode, wiz=False):
        production = self.browse(production_id)
        stock_mov_obj = self.env['stock.move']
        if wiz and production_mode == 'consume_produce':
            for produce_product in production.move_created_ids:
                produce_product.write({'location_dest_id':wiz.location_id.id})
        super(MrpProduction, self).action_produce(production_id, production_qty, production_mode, wiz)

    @api.model
    def _make_service_procurement(self, line):
        loc_obj = self.env['stock.location']
        proc_obj = self.env["procurement.order"]
        warh_obj = self.env["stock.warehouse"]
        if (line.product_id.need_procurement() and
                line.product_id.type == 'service' and
                line.product_id.seller_ids):
            source_location_id = line.production_id.location_src_id
            warehouse_id = loc_obj.get_warehouse(source_location_id)
            warehouse = warh_obj.browse(warehouse_id)
            vals = {
                'name': line.production_id.name,
                'origin': line.production_id.name,
                'company_id': line.production_id.company_id.id,
                'date_planned': line.production_id.date_planned,
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'product_uom': line.product_uom.id,
                'product_uos_qty': line.product_uos_qty,
                'product_uos': line.product_uos.id,
                'location_id': source_location_id.id,
                'warehouse_id': warehouse_id,
                'group_id': line.production_id.move_prod_id.group_id.id,
                'rule_id': warehouse.subcontract_pull_id and
                warehouse.subcontract_pull_id.id or
                warehouse.buy_pull_id.id
                }
            proc = proc_obj.create(vals)
            proc.run()
        else:
            super(MrpProduction, self)._make_service_procurement(line)

    @api.model
    def _make_consume_line_from_data(self, production, product, uom_id, qty,
                                     uos_id, uos_qty):
        if (production.bom_id.routing_id and
                production.bom_id.routing_id.location_id and
                production.bom_id.routing_id.location_id.id !=
                production.location_src_id.id):
            if production.bom_id.routing_id.supplier_id:
                my_context = dict(self.env.context)
                my_context['subcontract_partner'] = \
                    production.bom_id.routing_id.supplier_id.id
                return super(MrpProduction, self.with_context(my_context)).\
                    _make_consume_line_from_data(production, product, uom_id,
                                                 qty, uos_id, uos_qty)
        return super(MrpProduction, self).\
            _make_consume_line_from_data(production, product, uom_id,
                                         qty, uos_id, uos_qty)

    @api.model
    def _create_previous_move(self, move_id, product, source_location_id,
                              dest_location_id):
        routes = product.route_ids + product.categ_id.total_route_ids
        pull_obj = self.env['procurement.rule']
        pulls = pull_obj.search([('route_id', 'in', [x.id for x in routes]),
                                    ('location_id', '=', dest_location_id)], limit=1)

        if pulls.action == 'buy':
            # crear procurement en la ubicación
            stock_move = self.env['stock.move']
            type_obj = self.env['stock.picking.type']
            # Need to search for a picking type
            move = stock_move.browse(move_id)
            vals = {
                'name': move.name,
                'origin': move.name,
                'company_id': move.company_id.id,
                'date_planned': move.date_expected,
                'product_id': move.product_id.id,
                'product_qty': move.product_qty,
                'product_uom': move.product_uom.id,
                'product_uos_qty': move.product_uos_qty,
                'product_uos': move.product_uos.id,
                'location_id': dest_location_id
                }
            proc = self.env['procurement.order'].create(vals)
            self.env['procurement.order'].run( [proc],)
            return move.id
        else:
            move = super(MrpProduction, self)._create_previous_move(
                move_id, product, source_location_id,
                                      dest_location_id)
            if self.env.context.get('subcontract_partner', False):
                move_obj = self.env["stock.move"].browse(move)
                move_obj.write({'partner_id':
                                self.env.context['subcontract_partner']})
        return move


class MrpRouting(models.Model):

    _inherit = "mrp.routing"

    supplier_id = fields.Many2one('res.partner', 'Subcontract Supplier',
                                  domain=[("supplier", "=", True)],
                                  help="If you subcontract the manufacturing "
                                       "operations and you need to send "
                                       "goods to supplier, set it here")
