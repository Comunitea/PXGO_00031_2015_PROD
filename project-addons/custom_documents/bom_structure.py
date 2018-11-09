## -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.osv import osv
from openerp.report import report_sxw


class bom_structure(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_children': self.get_children,
        })

    def get_children(self, object, level=0):
        result = []

        def _get_rec(object, level):
            for l in object:
                seller = l.product_id.seller_ids and l.product_id.seller_ids[0] or False
                res = {}
                res['pname'] = l.product_id.name
                res['pcode'] = l.product_id.default_code
                res['pqty'] = l.product_qty
                res['uname'] = l.product_uom.name
                res['level'] = level
                res['code'] = l.bom_id.code
                res['supplier_ref'] = seller and seller.product_code
                res['supplier_name'] = seller and seller.product_name
                result.append(res)
                if l.child_line_ids:
                    if level < 6:
                        level += 1
                    _get_rec(l.child_line_ids, level)
                    if level > 0 and level < 6:
                        level -= 1
            return result

        children = _get_rec(object, level)

        return children


class ReportMrpBomStructure(osv.AbstractModel):
    _inherit = 'report.mrp.report_mrpbomstructure'
    _wrapped_report_class = bom_structure
