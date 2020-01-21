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
    'name': 'Custom documents',
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Pexego',
    'website': '',
    "depends": ['purchase', 'account', 'l10n_es_partner_mercantil',
                'account_payment_partner', 'sale',
                'report_qweb_element_page_visibility', 'sale_layout', 'printer_zpl2'],
    "data": ['views/footer.xml', 'views/header.xml',
             'views/report_purchaseorder.xml', 'views/report_invoice.xml',
             'views/report_saleorder.xml', 'views/report_stockpicking.xml',
             'views/sale.xml', 'views/stock.xml', 'views/account.xml',
             'views/valued_picking_report.xml', 'data/report_paperformat.xml',
             'sale_report.xml',
             'views/res_company.xml',
             'views/res_partner.xml',
             'views/report_mrpbomstructure.xml',
             'views/report_mrporder.xml',
             'views/report_product_zpl_label.xml',
             'wizard/product_print_labels.xml',
             'wizard/product_print_labels_from_picking.xml'],
    "installable": True
}
