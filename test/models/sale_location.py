from odoo import api, fields, models, _

class SaleOrder(models.Model):
	_inherit = "sale.order"

	sales_date = fields.Date(string='Line Date', copy=False)
	location_id = fields.Many2one("stock.location", string="Location", store=True)
