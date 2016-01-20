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
import openerp.addons.decimal_precision as dp


class ProductProduct(models.Model):

    _inherit = 'product.product'

    price_unit_distribution = fields.Float(
        'Distribution price unit', digits=dp.get_precision('Product Price'))
    sales_count = fields.Integer(compute='_sales_count')

    @api.one
    def _sales_count(self):
        self.sales_count = self.env['sale.order'].search_count(
            [('order_line.product_id', '=', self.id)])


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    _defaults = {
        'type' : 'product',
    }
