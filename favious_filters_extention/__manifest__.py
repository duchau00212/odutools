# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Faviours Extention',
    'category': 'Hidden',
    'version': '1.0',
    'author': 'Hauga',
    'description':
        """
Odoo Web core module.
========================

This module provides the core of the Odoo Web Client.
        """,
    'depends': ['web'],
    'auto_install': True,
    'data': [
        'view/template.xml',
    ],
    'qweb': [
        "static/xml/*.xml",
    ],
    'bootstrap': True,  # load translations for login screen
}
