{
    'name' : 'Odoo Pet Store',
    'version': '1.0',
    'summary': 'Sell pet toys',
    'category': 'Tools',
    'description':
        """
Odoo Pet Store
=================

A wonderful application to sell pet toys.
        """,
    'data': [
        "views/petstore.xml",       
    ],
    'demo': [
        "demo/petstore_data.xml",
        "demo/demo.xml",
        "demo/petstore.message_of_the_day.csv"
    ],
    'depends' : ['sale_stock'],
    'qweb': ['static/src/xml/petstore.xml'],
    'application': True,
}
