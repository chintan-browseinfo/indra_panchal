# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class MultiInvoicePayment(models.Model):
    _inherit = 'account.invoice'

