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

{
    'name': "Prodimar customizations",
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Pexego',
    'website': '',
    "depends": ['sale', 'stock', 'sale_stock', 'account', 'account_analytic_analysis'],
    "data": ['stock_view.xml', 'sale_order_view.xml', 'account_invoice.xml',
             'product_view.xml', 'wizard/stock_transfer_details_view.xml',
             'res_partner_view.xml', 'purchase_order.xml',
             'wizard/stock_drop.xml', 'res_company.xml',
             'wizard/postmigration_reconcile_quants_view.xml',
             'account_analytic_account.xml'],
    "installable": True
}
