from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    jyc_tracking_id = fields.Char('Tracking ID', related='picking_ids.jyc_tracking_id')