# -*- coding = utf - 8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import models, fields, api


class StockPicking(models.Model): 
    _inherit = "stock.picking"


    @api.model
    def get_provider_cat(self,id=False):
        flag=0
        stock_picking = self.env['stock.picking'].search([('id', '=', id)])
        for category in stock_picking.partner_id.category_id:
            if category.name=="Mayorista":
                flag=1
        if flag==1:
            return "Mayorista"
        else:
            return "otro"
