import time
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class ProductProduct(models.TransientModel):
	_name = 'wizard.product'

	product_list = fields.Many2one('product.template', string='Product')
	is_pack  = fields.Boolean(string='Is product pack',related="product_list.is_pack")
	product_pa_ids = fields.One2many('products', 'product_tmpl_id', string='Product Attributes')
	pack_qauntity = fields.Float(string='Pack Qauntity',default=1.0)
		
	def action_view_new_product(self):
		self.ensure_one()
		res = self.env['sale.order'].browse(self._context.get('active_id'))
		print "===========================res========================",res
		for product in self:
			k = []
			for i in product.product_list.product_pack_ids:
				k.append([0,0,{'product_id':i.product_id,'product_uom_qty':i.product_uom_qty*self.pack_qauntity}])
		res['order_line'] = k
		return

	@api.multi
	@api.onchange('product_list')
	def _onchange_product_list(self):
		self.ensure_one()
		print "========================================================="
		if self.product_list:
			k = []
			for i in self.product_list.product_pack_ids:
				print "i======================================",i
				k.append([0,0,{'product_id':i.product_id,'product_uom_qty':i.product_uom_qty}])
			self.product_pa_ids = k
		return


class Changepassword(models.TransientModel):
	_name = 'products'

	product_tmpl_id = fields.Many2one('wizard.product', string='Product Template',required=True)
	product_id = fields.Many2one('product.product', string='Product')
	product_uom_qty = fields.Float(string='Quantity')



