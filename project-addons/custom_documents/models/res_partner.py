# -*- coding: utf-8 -*-
# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    sale_text = fields.Text()
