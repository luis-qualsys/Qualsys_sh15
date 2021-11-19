# -*- coding: utf-8 -*-
{
    'name': "Validación de recepción con códigos de barras",

    'summary': """
        Validar la cantidad en la recepción.
        """,

    'description': """
        Este desarrollo valida las cantidades de compra 
        si la cantidad no sobrepasa cantidad en recepción.
    """,

    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",

    'category': 'Purchase',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 
                'purchase', 
                'stock',
                'barcodes',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            '/fer_barcode_validation/static/src/js/bar_validation_button.js',
            '/fer_barcode_validation/static/src/js/bar_validation_line.js',
            '/fer_barcode_validation/static/src/js/bar_validation_client.js',
        ]
    },
    # only loaded in demonstration mode
    'demo': [],
}
