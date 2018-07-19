from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOder1(models.Model):
	_inherit = 'sale.order'
	