# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multiple Invoice Payment',
    'version': '10.0.0.1',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'Demo',
    'author' : 'Browseinfo',
    'description': """Multiple Invoice Payment """,
    'website': '',
    'depends': ['account','account_accountant'],
    'data': [
    'wizard/multi_invoice_payment_views.xml',
    'views/multi_payment_views.xml',
    ],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
