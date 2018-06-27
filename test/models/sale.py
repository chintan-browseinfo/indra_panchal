from odoo import api, fields, models, _

class SaleOrder(models.Model):
	_inherit = "sale.order"

	month = fields.Char(String='Month')
	week = fields.Integer(String='Week')
	sales_date = fields.Date(String="Date")
	location_id = fields.Many2one("stock.location", string="Location", store=True)