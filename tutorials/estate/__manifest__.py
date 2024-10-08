{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Manage properties and estates',
    'description': 'Module to manage properties, estates, and related functionalities.',
    'category': 'Real Estate',
    'author': 'Muntadhar',

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_menus.xml'
    ],

    'installable': True,
    'application': True,  # Set this to True if it is a standalone app
}
