import time
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class Changepassword(models.TransientModel):
	_name = 'changepassword.module'

	real_password = fields.Char(String="Old Password")
	create_password = fields.Char(String='Create Password')
	confirm_password = fields.Char(String='Confirm Password')
	
	@api.model
	def default_get(self, default_fields):
		res = super(Changepassword, self).default_get(default_fields)
		pas = self.env['studentapplication.module'].browse(self._context.get('active_id'))
		res['real_password'] = pas.password
		return res

	@api.multi
	def change_inquiry_password(self):
		pas = self.env['studentapplication.module'].browse(self._context.get('active_id'))
		if self.create_password == self.confirm_password:
			pas.password = self.create_password
		else:
			raise UserError(_("password didn't matched..........."))
			pas.password = self.real_password
			return
		return
