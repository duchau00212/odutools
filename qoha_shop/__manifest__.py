# -*- coding: utf-8 -*-
{
    'name' : 'Qoha shop',
    'version' : '1.0',
    'summary': 'Customize Ecommerce by Qoha shop',
    'description': """""",
    'author': 'HauTran!',
    'category': 'Accounting',
    'website': 'https://www.google.com.vn',
    'depends' : ['website_sale', "website_portal"],
    'data': [
             #'views/sale_order.xml',
             'views/template.xml',
             'views/report.xml',
    ],
    #'qweb': [
    #    "static/src/xml/shop_backend.xml",
    #],
    'installable': True,
    'application': True,
    'auto_install': False,
}