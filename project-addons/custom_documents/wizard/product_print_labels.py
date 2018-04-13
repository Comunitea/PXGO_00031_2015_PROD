# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _


class ProductPrintLabels(models.TransientModel):

    _name = 'product.print.labels'

    location = fields.Many2one('stock.location', required=True)

    @api.multi
    def print_label(self):
        self.ensure_one()
        datas = {'ids': self._context.get('active_ids', [])}
        res = {'location': ' / '.join(self.location.complete_name.split(' / ')[1:])}
        datas['form'] = res
        return self.env['report'].get_action(
            self, 'custom_documents.report_product_label', data=datas)
