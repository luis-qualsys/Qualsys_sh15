import requests
from odoo import models, fields, _
from odoo.exceptions import UserError
from pprint import pprint

class ResCompany(models.Model):
    _inherit = 'res.company'

    jyc_ivoy_shop_name = fields.Char('Nombre del almacen iVoy')
    jyc_ivoy_referenceId = fields.Char('Referencia ID')
    jyc_ivoy_description = fields.Char('Descripción')
    jyc_ivoy_instructions = fields.Char('Instrucciones')
    jyc_ivoy_contact = fields.Char('Nombre de Contacto')
    jyc_ivoy_latitude = fields.Float('Latitud', related='partner_id.partner_latitude')
    jyc_ivoy_longitude = fields.Float('Longitud', related='partner_id.partner_longitude')
    jyc_ivoy_warehouse_id = fields.Char('ID iVoy Almacen')

    def get_warehouse_ivoy(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        auth = ICPSudo.get_param('jyc_ivoy_api.auth_bearer')
        user = ICPSudo.get_param('jyc_ivoy_api.x_voy_user')
        url = "https://api.ivoy.mx/graphql"
        payload = {
            "query": "mutation createStore($inputStore: CreateStoreInput!){createStore(input: $inputStore){id}}",
            "variables": {"inputStore": {
                    "name": f"{self.jyc_ivoy_shop_name}",
                    "referenceId": f"{self.jyc_ivoy_referenceId}",
                    "description": f"{self.jyc_ivoy_description}",
                    "location": {
                        "address": f"{self.street_name or ''} {self.street_number or ''} {self.street_number2 or ''}, {self.l10n_mx_edi_colony or ''}, {self.zip or ''} {self.city or ''}",
                        "zipCode": f"{self.zip or ''}",
                        "instructions": f"{self.jyc_ivoy_instructions}",
                        "latitude": self.jyc_ivoy_latitude,
                        "longitude": self.jyc_ivoy_longitude
                    },
                    "contact": {
                        "name": f"{self.jyc_ivoy_contact}",
                        "phone": f"{self.mobile}",
                        "email": f"{self.email}"
                    }
                }}
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth}",
            "x-ivoy-user": f"{user}"
        }
        
        pprint(payload)

        try:
            response = requests.request("POST", url, json=payload, headers=headers)

            print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                respuesta = response.json()
                print(respuesta['data']['createStore']['id'])
                self.jyc_ivoy_warehouse_id = respuesta['data']['createStore']['id']
            else:
                self.jyc_ivoy_warehouse_id = ''
                raise UserError(_('Error al hacer la petición.'))
        except Exception as e:
            self.jyc_ivoy_warehouse_id = ''
            raise UserError(_('Error al hacer la petición.', e))