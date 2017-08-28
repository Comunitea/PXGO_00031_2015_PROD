# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _


class ProductPrintLabelsFromPicking(models.TransientModel):

    _name = 'product.print.labels.from.picking'

    @api.multi
    def print_label(self):
        self.ensure_one()
        datas = {'ids': self.env['stock.picking'].browse(
            self._context['active_ids']).mapped('pack_operation_ids.id')}
        return self.env['report'].get_action(
            self, 'custom_documents.report_product_label_from_picking',
            data=datas)
