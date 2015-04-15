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

{
    'name': 'MRP Subcontracting',
    'version': '1.0',
    'category': '',
    'description': """Improves mrp workflow for subcontracting orders""",
    'author': 'Pexego',
    "depends": ['purchase', 'mrp', 'product', 'stock'],
    "data": ['data/mrp_subcontract_data.xml',
             'views/stock_view.xml',
             'views/mrp_view.xml'],
    "installable": True
}
