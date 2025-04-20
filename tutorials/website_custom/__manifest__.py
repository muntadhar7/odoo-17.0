{
    'name': 'Website Custom',
    'version': '1.0',
    'summary': 'Adds map to checkout process',
    'depends': ['website', 'website_sale'],
    'data': [
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_custom/static/src/js/geo_checkout.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}