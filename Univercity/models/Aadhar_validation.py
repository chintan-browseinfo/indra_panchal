from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PersonAadhar(models.Model):
	_inherit= 'res.partner'
	
	aadhar = fields.Char(String='Aadhar Card') 

	@api.model
	def create(self,vals):
	  	print "===============vals==============",vals
		
		a_id = self.env['res.partner'].browse(vals.get('aadhar'))
		print "===============a_id===========",a_id
		if not a_id:
			raise ValidationError(_('Configuration error!\nEnter aadhar card Number.'))
		if a_id:
			if not len(vals.get('aadhar')) == 12:
				raise ValidationError(_('Configuration error!\nEnter Valid aadhar card Number \n aadhar number must be 12 digit.'))
					
		val_id = self.env['res.partner'].search([('aadhar', '=', vals.get('aadhar') )])
		if val_id:
			raise ValidationError(_('Configuration error!\naadhar already exists.'))

		aadhar = super(PersonAadhar,self).create(vals)
		return aadhar


	@api.multi
	def write(self,vals):
		print "===============vals==============",vals
		aa_id = self.env['res.partner'].browse(vals.get('aadhar'))
		if aa_id:
			if not len(vals.get('aadhar')) == 12:
				raise ValidationError(_('Configuration error!\nEnter Valid aadhar card Number \n aadhar number must be 12 digit.'))
					
		if aa_id:
			vals_id = self.env['res.partner'].search([('aadhar', '=', vals.get('aadhar') )])
			if vals_id:
				raise ValidationError(_('Configuration error!\naadhar already exists.'))

		aadhar = super(PersonAadhar,self).write(vals)
		return aadhar