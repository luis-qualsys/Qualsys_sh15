# -*- coding: utf-8 -*-
{
    'name': "API ondemand de iVoy",

    'summary': """
        Conecta los servicios de iVoy con el módulo de entregas de Odoo para enviar el Tracking ID
        """,

    'description': """
        Este desarrollo permite conectar los servicios de iVoy con el módulo
        de entregas de Odoo para enviar el Tracking ID, tambien agrega las 
        vistas necesarias para que el usuario visualize el trackin ID
    """,

    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 
                'sale',
                ],

    # always loaded
    'data': [
        'views/stock_picking_inherit_views.xml',
        'views/settings.xml',
        'views/res_company_inherit_views.xml',
        # 'views/template_portal_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'license': 'LGPL-3',
}
