# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ReportProductLabel(models.AbstractModel):
    _name = 'report.custom_documents.report_product_label'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'custom_documents.report_product_label')
        docs = self.env['product.product'].browse(data['ids'])
        docargs = {
            'doc_ids': data['ids'],
            'doc_model': report.model,
            'docs': docs,
            'data': data,
            'location': data['form']['location']
        }
        return report_obj.render('custom_documents.report_product_label',
                                 docargs)


class ReportProductLabelFromPicking(models.AbstractModel):
    _name = 'report.custom_documents.report_product_label_from_picking'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'custom_documents.report_product_label_from_picking')
        docs = self.env['stock.pack.operation'].browse(data['ids'])
        docargs = {
            'doc_ids': data['ids'],
            'doc_model': report.model,
            'docs': docs,
            'data': data
        }
        return report_obj.render('custom_documents.report_product_label_from_picking',
                                 docargs)
