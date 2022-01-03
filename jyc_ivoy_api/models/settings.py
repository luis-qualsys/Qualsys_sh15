# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class iVoyTrackingSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auth_bearer = fields.Char(string="Autorización Bearer")
    x_voy_user = fields.Char(string="x_voy_user")
    api_type = fields.Selection(string="Tipo de servicio API", selection=[
        ('ON_DEMAND', 'On Demand'),
        ('NEXT_DAY', 'Next Day'),
        ('SAME_DAY', 'Same Day')
        ])

    def set_values(self):
        res = super(iVoyTrackingSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('jyc_ivoy_api.auth_bearer', self.auth_bearer)
        self.env['ir.config_parameter'].set_param('jyc_ivoy_api.x_voy_user', self.x_voy_user)
        self.env['ir.config_parameter'].set_param('jyc_ivoy_api.api_type', self.api_type)

        return res

    @api.model
    def get_values(self):
        res = super(iVoyTrackingSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        auth_bearer = str(ICPSudo.get_param('jyc_ivoy_api.auth_bearer'))
        x_voy_user = str(ICPSudo.get_param('jyc_ivoy_api.x_voy_user'))
        api_type = str(ICPSudo.get_param('jyc_ivoy_api.api_type'))

        res.update(
            auth_bearer = auth_bearer,
            x_voy_user = x_voy_user,
            api_type = api_type
        )
        return res