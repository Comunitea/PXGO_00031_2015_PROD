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

class stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    account_analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account', related='packop_id.linked_move_operation_ids.move_id.purchase_line_id.account_analytic_id', readonly=True)


class stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(stock_transfer_details,self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        picking_id = self._context.get('active_id', False)
        picking = self.env['stock.picking'].browse(picking_id)
        if picking.picking_type_code != 'incoming':
            arch = res.get('fields', {}).get('item_ids', {}).get('views', {}).get('tree', {}).get('arch', '')
            if not arch:
                return res
            doc = etree.XML(arch)
            node_me = doc.xpath("//field[@name='account_analytic_id']")[0]
            node_me.getparent().remove(node_me)
            res['fields']['item_ids']['views']['tree']['arch'] = etree.tostring(doc)
        return res

