# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def manual_force_done(self):
        for order in self:
            if order.state != 'done':
                order.state = 'done'

    def onchange_picking_type_id(self, cr, uid, ids, picking_type_id, context=None):
        value = {}
        if picking_type_id:
            picktype = self.pool.get("stock.picking.type").browse(cr, uid, picking_type_id, context=context)
            if picktype.default_location_dest_id:
                value.update({'location_id': picktype.default_location_dest_id.id, 'related_usage': picktype.default_location_dest_id.usage})
            value.update({'related_location_id': picktype.default_location_dest_id.id})
        if value.get('related_usage') != 'customer':
            value['dest_address_id'] = None
        return {'value': value}

    def onchange_location_id(self, cr, uid, ids, location_id, context=None):
        value = {'related_usage': False}
        if location_id:
            value['related_usage'] = self.pool['stock.location'].browse(cr, uid, location_id, context=context).usage
        if value['related_usage'] != 'customer':
            value['dest_address_id'] = None
        return {'value': value}
