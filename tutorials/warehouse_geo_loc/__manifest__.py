{
    'name': 'Warehouse Geo Location',
    'version': '1.0',
    'author': 'Muntadhar',
    'summary': '',
    'description': '.',
    'category': '',
    'data': [
        'security/ir.model.access.csv',
        'views/warehouse_geo_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'warehouse_geo_loc/static/src/js/google_map.js',  # Your custom JS file
        ],
    },
    'installable': True,
    'application': False,
    'depends': ['stock', 'web', 'base_setup'],
}