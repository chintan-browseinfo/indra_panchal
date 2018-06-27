# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sample',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 120,
    'summary': 'Sample Module for Trainees',
    'description': """Test Module
    """,
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'sale','stock'],
    'data': ['views/sample_views.xml',
            'views/sale_location_views.xml',
            'views/sale_views.xml',
            'views/sale_tree_views.xml',
            'views/sale_date_views.xml',],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
