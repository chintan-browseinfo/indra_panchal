from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class TestModel(models.Model):
	_name = "product"

	product_packs_id = fields.Many2one('product.template', string='Product Template')
	product_id = fields.Many2one('product.product', string='Product')
	product_uom_qty = fields.Float(string='Quantity')

class ProductProduct(models.Model):
	_inherit = 'product.template'

	@api.multi
	@api.onchange('compute_price','product_pack_ids')
	def _onchange_product_pack(self):
		self.ensure_one()
		if not self.compute_price:
			return		
		total = 0 
		for i in self:
			print "i=========================================",i
			for product in i.product_pack_ids:
				print "=================================================",product
				total += (product.product_uom_qty * product.product_id.lst_price)
				print "=================================================",total
			i.list_price = total
		return

	product_pack_ids = fields.One2many('product', 'product_packs_id')	
	is_pack = fields.Boolean(string="IS Product Pack")
	compute_price = fields.Boolean(string="Compute Price",default=False)

	