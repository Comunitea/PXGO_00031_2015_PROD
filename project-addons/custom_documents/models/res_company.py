# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    gdpr_text = fields.Text()
