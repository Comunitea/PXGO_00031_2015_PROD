# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class ProductPrintLabelsFromPicking(models.TransientModel):

    _name = 'product.print.labels.from.picking'

    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Printer', required=True,
        help='Printer used to print the labels.')

    @api.multi
    def print_label(self):
        self.ensure_one()
        for pack_operation in self.env['stock.picking'].browse(
                self._context['active_ids']).mapped('pack_operation_ids'):
            wizard = self.env['wizard.print.record.label'].create({
                'printer_id': self.printer_id.id,
                'label_id':
                self.env.ref('custom_documents.product_product_zpl_label').id,
            })
            location_name = pack_operation.location_dest_id.name
            wizard.with_context(
                location_name=location_name,
                active_ids=[pack_operation.product_id.id],
                active_model='product.product').print_label()
