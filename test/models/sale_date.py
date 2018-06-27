from odoo import api, fields, models, _

class SaleOder1(models.Model):
	_inherit = 'sale.order'

	date = fields.Date(String='Date', copy=False)

class SaleOrder(models.Model):
	_inherit = 'sale.order.line'

	date = fields.Date(String='Date', copy=False)