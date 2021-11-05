from odoo import api, fields, models, _
from odoo.exceptions import UserError

class FerStockWarehouseOrderpointEfim(models.Model):
    _name = 'fer.stock.warehouse.orderpoint.efim'
    _description = 'Stock valores efimeros'

    product_id = fields.Many2one('product.product', string='Producto', required=True, domain=[('type', 'ilike', 'product')])
    fer_brand_name = fields.Char('Marca', compute='get_brand_name')
    location_id = fields.Many2one('stock.location', string='Ubicación', store=True)
    fer_c_product_min = fields.Integer('Cal mínima', default=0)
    fer_c_product_max = fields.Integer('Cal máxima', default=0)
    fer_old_product_min = fields.Integer(string='Hist mínima', default=0, store=True)
    fer_old_product_max = fields.Integer(string='Hist máxima', default=0, store=True)
    fer_history_stock_orderpoint_ids = fields.Many2one('fer.history.stock.orderpoint', string="Historial de reglas abastecimiento")

    # Data saved
    fer_product_average = fields.Float(string='Valor promedio')
    fer_product_cumulative = fields.Float(string='Valor acumulado')
    fer_product_letter = fields.Char(string='Letra')
    fer_product_participation = fields.Float(string='Participación')
    fer_qty_done = fields.Float(string='Unidades vendidas')

    @api.depends('product_id')
    def get_brand_name(self):
        for record in self:
            if record.product_id:
                product = self.env['product.template'].search([('id', '=', record.product_id.product_tmpl_id.id)])[0]
                
                if product.id:
                    record.fer_brand_name = product.fer_brand_ids.fer_brand_name
                else:
                    record.fer_brand_name = ''
            else:
                record.fer_brand_name = ''
                continue

    @api.onchange('product_id')
    # @api.depends('product_id')
    def _onchange_product_id(self):
        rules = self.env['stock.warehouse.orderpoint'].search([
            ('product_id', '=', self.product_id.id)
            ])
        if self.product_id:
            print(rules)
            for rule in rules:
                if rule.id:
                    if self.fer_history_stock_orderpoint_ids.location_id in rule.location_id.display_name:
                        self.location_id = rule.location_id.id,
                        self.fer_old_product_min = rule.product_min_qty
                        self.fer_old_product_max = rule.product_max_qty
                    else:
                        self.location_id = ''
                        self.fer_old_product_min = 0
                        self.fer_old_product_max = 0
                else:
                    raise UserError(_('El producto seleccionado debe tener una regla de reordenamiento configurada.'))

    


        # for record in self:
        #     # print(record.fer_history_stock_orderpoint_ids.location_id)
        #     record_id = self.env['fer.stock.warehouse.orderpoint.efim'].search([
        #         ('id', '=', record.id)
        #         ])[0]
        #     rules = self.env['stock.warehouse.orderpoint'].search([
        #         ('product_id', '=', record.product_id.id)
        #         ])
        #     if len(rules) >= 1:
        #         for rule in rules:
        #             if record.fer_history_stock_orderpoint_ids.location_id in rule.location_id.display_name:
        #                 record.location_id = rule.location_id.id,
        #                 record.fer_old_product_min = rule.product_min_qty
        #                 record.fer_old_product_min = rule.product_max_qty