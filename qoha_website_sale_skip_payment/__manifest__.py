# -*- coding: utf-8 -*-
{
    'name' : 'Website sale skip payment method',
    'version' : '1.0',
    'summary': 'Customize Ecommerce by Qoha shop',
    'description': """""",
    'author': 'HauTran!',
    'category': 'Accounting',
    'website': 'https://www.google.com.vn',
    'depends' : ['sale', 'website_sale', "website_portal", "website_portal_sale"],
    'data': [
             'views/sale_order.xml',
             'views/template.xml',
    ],
    #'qweb': [
    #    "static/src/xml/shop_backend.xml",
    #],
    'installable': True,
    'application': True,
    'auto_install': False,
}