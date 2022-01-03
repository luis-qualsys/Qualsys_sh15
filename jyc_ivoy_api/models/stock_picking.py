import requests
from pprint import pprint
from odoo import models, fields, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    jyc_tracking_id = fields.Char('Tracking iVoy ID', readonly=True)
    jyc_altura = fields.Float('Altura cm', default=0.0)
    jyc_ancho = fields.Float('Ancho cm', default=0.0)
    jyc_longitud = fields.Float('Longitud cm', default=0.0)
    jyc_peso = fields.Float('Peso kg', default=0.0)
    jyc_description = fields.Char('Descripción')
    jyc_cantidad = fields.Integer('Cantidad', default=0)

    def validate_with_tracking_id_ivoy(self):
        for move_ids in self.move_ids_without_package:
            if move_ids.quantity_done == 0:
                print(move_ids)
                raise UserError(_('No se puede validar una transferencia si no se reservan ni se hacen cantidades. Para forzar el traslado, cambie al modo de edición y codifique las cantidades hechas.'))
        
        if self.jyc_cantidad == 0 or self.jyc_longitud == 0 or self.jyc_ancho == 0 or self.jyc_peso == 0:
            raise UserError(_('Favor de poner los detalles del paquete.'))
        else:
            if not self.jyc_tracking_id:
                if self.env.company.jyc_ivoy_warehouse_id:
                    self.partner_id.geo_localize()
                    if self.partner_id.partner_latitude == 0 or self.partner_id.partner_longitude == 0:
                        raise UserError(_('Favor de verificar la dirección de entrega'))
                    else:
                        self.partner_id.geo_localize()
                        almacenID = self.env.company.jyc_ivoy_referenceId
                        street = self.partner_id.street_name or ''
                        number = self.partner_id.street_number or ''
                        number2 = self.partner_id.street_number2 or ''
                        colony = self.partner_id.l10n_mx_edi_colony or ''
                        city = self.partner_id.city or ''
                        state = self.partner_id.state_id.name or ''
                        zip_code = self.partner_id.zip or ''
                        referencia = self.sale_id.client_order_ref or ''
                        name = self.partner_id.name
                        email = self.partner_id.email
                        phone = self.partner_id.phone
                        latitude = self.partner_id.partner_latitude
                        longitude = self.partner_id.partner_longitude
                        altura = self.jyc_altura
                        ancho = self.jyc_ancho
                        longitud = self.jyc_longitud
                        peso = self.jyc_peso
                        descripcion = self.jyc_description
                        cantidad = self.jyc_cantidad
                        trackingNumber = self.get_tracking_id_ivoy(almacenID, street, number, number2, colony, city, state, zip_code, referencia, name, email, phone, latitude, longitude, altura, ancho, longitud, peso, descripcion, cantidad)
                        self.jyc_tracking_id = trackingNumber

                        res = super(StockPicking, self).button_validate()
                        return res
                else:
                    raise UserError(_('No a configurado un almacen de iVoy.'))
            else:
                raise UserError(_('Ya tiene configurado un Tracking ID iVoy.'))
        

    def get_tracking_id_ivoy(self, almacenID, street, number, number2, colony, city, state, zip_code, referencia, name, email, phone, latitude, longitude, altura, ancho, longitud, peso, descripcion, cantidad):
        print('GET tracking ivoy ID')
        ICPSudo = self.env['ir.config_parameter'].sudo()
        auth = ICPSudo.get_param('jyc_ivoy_api.auth_bearer')
        user = ICPSudo.get_param('jyc_ivoy_api.x_voy_user')
        type_api = ICPSudo.get_param('jyc_ivoy_api.api_type')
        url = "https://api.ivoy.mx/graphql"
        payload = {
                "query": "mutation createDelivery($input: CreateDeliveryInput!){createDeliveryWithLabel(input: $input){id trackingNumber referenceId label(type: ZPL)}}",
                "variables": {"input": {
                        "type": f"{type_api}",
                        "referenceId": f"{'-'.join(name.split(' ')[:2])}-Guia",
                        "storeId": f"{almacenID}",
                        "dropoff": {
                            "location": {
                                "address": f"{street} {number} {number2}, {colony}, {city}, {zip_code} {state}, CDMX",
                                "zipCode": f"{zip_code}",
                                "latitude": latitude,
                                "longitude": longitude,
                                "instructions": f"{referencia}"
                            },
                            "contact": {
                                "name": f"{name}",
                                "phone": f"{phone}",
                                "email": f"{email}"
                            }
                        },
                        "packages": [
                            {
                            "dimensions": {
                                "height": altura,
                                "width": ancho,
                                "length": longitud,
                                "weight": peso
                            },
                            "items": [
                                {
                                    "description": f"{descripcion}",
                                    "quantity": cantidad
                                }
                            ]
                            }
                        ]
                    }}
            }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth}",
            "x-ivoy-user": f"{user}"
        }


        response = requests.request("POST", url, json=payload, headers=headers)
        respuesta = response.json()
        print(respuesta)
        print(response.text)
        if response.status_code == 200 and respuesta['data']['createDeliveryWithLabel']['trackingNumber'] != '':
            trackingNumber = respuesta['data']['createDeliveryWithLabel']['trackingNumber']
            return trackingNumber
        elif response.status_code == 400:
            raise UserError(_('Error en la petición. %s' % respuesta['errors'][0]['message']))
    
    def send_tracking_id_ivoy(self):
        pass