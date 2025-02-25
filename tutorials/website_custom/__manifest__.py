{
    'name': 'Website Customization',
    'version': '17.0.1.0',
    'summary': 'Custom modifications for the Odoo 17 website',
    'author': 'Muntadhar',
    'category': 'Website',
    'depends': ['website'],
    'data': [
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_custom/static/src/js/location.js',
        ],
    },
    'installable': True,
    'application': False,
}
