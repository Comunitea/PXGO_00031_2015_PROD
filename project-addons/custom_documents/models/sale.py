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
from openerp import models, fields, api
from datetime import datetime


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_order_without_hour = fields.Date('Date order',
                                          compute='_get_date_order_qweb',
                                          store=True)
    title = fields.Char('Title')
    only_total_all_lines = fields.Boolean(compute='_get_only_total_lines')

    @api.multi
    def _get_only_total_lines(self):
        for obj in self:
            obj.only_total_all_lines = all(obj.mapped(
                'order_line.report_only_total'))

    @api.one
    @api.depends('date_order')
    def _get_date_order_qweb(self):
        datetime_date_order = datetime.strptime(self.date_order,
                                                '%Y-%m-%d %H:%M:%S')
        self.date_order_without_hour = datetime_date_order.date()

    @api.multi
    def action_ship_create(self):
        res = super(SaleOrder, self).action_ship_create()
        for obj in self:
            for move in obj.mapped('picking_ids.move_lines'):
                move.report_only_total = \
                    move.procurement_id.sale_line_id.report_only_total
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    report_only_total = fields.Boolean('Only total')
