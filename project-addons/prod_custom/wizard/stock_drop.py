# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class StockDrop(models.TransientModel):

    _name = 'stock.drop'

    lines = fields.One2many('stock.drop.line', 'drop')
    warehouse = fields.Many2one('stock.warehouse')
    warehouse_location = fields.Many2one('stock.location',
                                         related='warehouse.view_location_id',
                                         readonly=True)

    @api.multi
    def move(self):
        self.ensure_one()
        allowed_locations = self.env['stock.location'].search(
            [('id', 'child_of', self.warehouse.view_location_id.id)])
        picking_vals = {
            'picking_type_id': self.warehouse.int_type_id.id,
        }
        move_list = []
        for line in self.lines:
            if line.location not in allowed_locations:
                raise exceptions.Warning(
                    _('Location error'),
                    _('The location %s does not belong to warehouse %s') %
                    (line.location.name, self.warehouse.name))
            move_list.append(
                (0, 0,
                 {'product_id': line.product.id,
                  'product_uom_qty': line.quantity,
                  'product_uom': line.product.uom_id.id,
                  'location_id': line.location.id,
                  'location_dest_id':
                      self.env.user.company_id.drop_location.id,
                  'name': line.product.partner_ref,
                  }))
        picking_vals['move_lines'] = move_list
        new_picking = self.env['stock.picking'].create(picking_vals)
        new_picking.action_confirm()
        new_picking.action_assign()
        if new_picking.state != 'assigned':
            error_msg = ''
            for move in new_picking.move_lines:
                if move.state != 'assigned':
                    error_msg += _('\nNot found enought stock in %s for product %s') % (move.location_id.name, move.product_id.name)
            raise exceptions.Warning(_('Quantity error'), error_msg)
            new_picking.action_done()
        action = self.env.ref('stock.action_picking_tree_all')
        if not action:
            return
        action = action.read()[0]
        res = self.env.ref('stock.view_picking_form')
        action['views'] = [(res.id, 'form')]
        action['res_id'] = new_picking.id
        action['context'] = False
        return action


class StockDropLine(models.TransientModel):

    _name = 'stock.drop.line'

    drop = fields.Many2one('stock.drop')
    product = fields.Many2one('product.product')
    quantity = fields.Float(digits=dp.get_precision('Product Unit of Measure'))
    location = fields.Many2one('stock.location')
