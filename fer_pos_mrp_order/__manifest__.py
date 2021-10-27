{
    'name': 'MRP orden de POS',
    'version': '13.0.1.0.3',
    'summary': """Generar una MRP orden despues de vender en POS.""",
    'description': """Generar una MRP orden despues de vender en POS.""",
    'author': 'Qualsys Consulting',
    'company': 'Qualsys Consulting',
    'website': 'https://www.qualsys.com.mx',
    'category': 'Point of Sale',
    'depends': ['point_of_sale', 'mrp', 'stock'],
    # 'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        # 'views/pos_template.xml',
    ],
    "assets": {
        "point_of_sale.assets": [
            "/fer_pos_mrp_order/static/src/js/models.js"
        ]},
    # 'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
