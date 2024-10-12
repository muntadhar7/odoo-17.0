{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Manage property_ids and estates',
    'description': 'Module to manage property_ids, estates, and related functionalities.',
    'category': 'Sales',
    'author': 'Muntadhar',

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_menus.xml',
        'views/res_users_views.xml',
    ],

    'installable': True,
    'application': True,  # Set this to True if it is a standalone app
}
