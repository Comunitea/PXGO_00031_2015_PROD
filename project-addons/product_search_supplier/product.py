# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    supplier_code_ref = fields.Char('Supplier ref',
                                    compute='_get_supplier_code', store=True)
    supplier_name_ref = fields.Char('Supplier ref',
                                    compute='_get_supplier_name', store=True)

    @api.multi
    @api.depends('seller_ids', 'seller_ids.product_code')
    def _get_supplier_code(self):
        for product in self:
            product.supplier_code_ref = ','.join(
                [x.product_code for x in product.seller_ids if x.product_code])

    @api.multi
    @api.depends('seller_ids', 'seller_ids.product_name')
    def _get_supplier_name(self):
        for product in self:
            product.supplier_name_ref = ','.join(
                [x.product_name for x in product.seller_ids if x.product_name])
