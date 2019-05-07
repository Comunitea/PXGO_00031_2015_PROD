# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _


class ProductPrintLabels(models.TransientModel):

    _name = 'product.print.labels'

    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Printer', required=True,
        help='Printer used to print the labels.')
    location = fields.Many2one('stock.location', required=True)
    location_name = fields.Char(compute='_compute_location_name')

    @api.one
    def _compute_location_name(self):
        self.location_name = ' / '.join(
            self.location.complete_name.split(' / ')[1:])

    @api.multi
    def print_label(self):
        self.ensure_one()
        wizard = self.env['wizard.print.record.label'].create({
            'printer_id': self.printer_id.id,
            'label_id': self.env.ref('custom_documents.product_product_zpl_label').id,
        })
        return wizard.with_context(location_name=self.location_name).print_label()
