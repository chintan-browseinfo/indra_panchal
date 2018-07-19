from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class TestModel(models.Model):
	_name = "product"

	product_packs_id = fields.Many2one('product.template', string='Product Template')
	product_id = fields.Many2one('product.product', string='Product')
	product_uom_qty = fields.Float(string='Quantity')


class ProductProduct(models.Model):
	_inherit = 'product.template'

	product_pack_ids = fields.One2many('product', 'product_packs_id')	
	is_pack = fields.Boolean(string="IS Product Pack")