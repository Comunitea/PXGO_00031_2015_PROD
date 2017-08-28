# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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
from openerp import models, fields, api, exceptions, _, tools


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    version = fields.Integer('Version', default=1, copy=False)
    base_version = fields.Many2one('sale.order', 'Base version', copy=False)
    version_ids = fields.One2many('sale.order', compute='_get_versions', string='Versions')
    active = fields.Boolean('Active', default=True)
    name = fields.Char(states={'draft': [('readonly', False)]})
    date_order = fields.Datetime(states={'draft': [('readonly', False)]})
    user_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_invoice_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_shipping_id = fields.Many2one(states={'draft': [('readonly', False)]})
    order_policy = fields.Selection(states={'draft': [('readonly', False)]})
    pricelist_id = fields.Many2one(states={'draft': [('readonly', False)]})
    project_id = fields.Many2one(states={'draft': [('readonly', False)]})
    order_line = fields.One2many(states={'draft': [('readonly', False)]})


    @api.multi
    @api.depends('base_version')
    def _get_versions(self):
        for sale in self:
            if not sale.base_version:
                sale.version_ids = False
                continue
            versions = self.search(
                [('base_version', '=', sale.base_version.id),
                 ('id', '!=', sale.id), '|', ('active', '=', True),
                 ('active', '=', False)])
            sale.version_ids = versions

    @api.multi
    def create_new_version(self):
        max_version = max([x.version for x in self.version_ids + self])
        args = {'version': max_version + 1, 'name': self.base_version.name + ' V' + str(max_version + 1),
                'base_version': self.base_version.id, 'active': True}
        new_version = self.copy(args)
        self.write({'active': False})
        action = self.env.ref('sale.action_quotations')
        if not action:
            return
        action = action.read()[0]
        res = self.env.ref('sale.view_order_form')
        action['views'] = [(res.id, 'form')]
        action['res_id'] = new_version.id
        action['context'] = False
        return action

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if not res.base_version:
            res.base_version = res.id
        return res

    @api.multi
    def action_button_confirm(self):
        if not self.active:
            raise exceptions.Warning(_('Order versioned'), _('can not confirm an order with new versions'))
        return super(SaleOrder, self).action_button_confirm()

    @api.multi
    def print_quotation(self):
        if not self.active:
            raise exceptions.Warning(_('Order versioned'), _('can not print an order with new versions'))
        return super(SaleOrder, self).print_quotation()

    @api.multi
    def action_quotation_send(self):
        if not self.active:
            raise exceptions.Warning(_('Order versioned'), _('can not send an order with new versions'))
        return super(SaleOrder, self).action_quotation_send()


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    active = fields.Boolean('Active', default=True)
    user_id = fields.Many2one('res.users', '', related='order_id.user_id',
                              store=True)

class sale_report(models.Model):
    _inherit = "sale.report"

    def init(self, cr):
        # self._table = sale_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE s.active=true
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))
