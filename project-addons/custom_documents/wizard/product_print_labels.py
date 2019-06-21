# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class ProductPrintLabels(models.TransientModel):

    _name = 'product.print.labels'

    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Printer', required=True,
        help='Printer used to print the labels.')
    location = fields.Many2one('stock.location', required=True)
    number_of_copies = fields.Integer(default=1)

    @api.multi
    def print_label(self):
        self.ensure_one()
        wizard = self.env['wizard.print.record.label'].create({
            'printer_id': self.printer_id.id,
            'label_id': self.env.ref(
                'custom_documents.product_product_zpl_label').id,
        })
        for i in range(self.number_of_copies):
            wizard.with_context(location_name=self.location.name).print_label()
