from odoo import models, api, fields, _
from datetime import datetime, timedelta

class StudentInquiry(models.Model):
	_name="studentachievement.module"

	name = fields.Char(String='Name of Achievemnet')
	achievement_id =  fields.Many2one('studentinquiry.module',String="Achievement List")
	achievement_level = fields.Selection((('taluka','taluka'),
		('jila','jila'),
		('state','state'),
		('national','national'),
		('international','international')),String="Achievement Level")


	@api.multi
	def _update_value(self,confirm=True, data=None):
		Registration = self.env['studentinquiry.module'].browse(self._context.get('active_id'))
 		print "Registration===========================",Registration
		# registrations = Registration.search([('achievement_id', 'in', self.ids)])
		for so_line in self.filtered('achievement_id'):
			print "so_line=====================",so_line,so_line.name,so_line.achievement_level	
			if data:
				data.pop()
			registration = {}
			registration['achievement_id'] = so_line.achievement_id
			registration['name'] = so_line.name
			registration['achievement_level'] = so_line.achievement_level		
		return True

	# @api.multi
	# def _update_val(self):
	# 	Reg = self.env['change.inquiry.achievement'].browse(self._context.get('active_id'))
 # 		print "Reg====================================",Reg
 # 		for so_line in self.filtered('achievement_id'):
 # 			print "so_line=====================",so_line,so_line.name,so_line.achievement_level	
	# 		registration = {}
	# 		# registration['achievement_id'] = so_line.achievement_id
	# 		registration['name'] = so_line.name
	# 		registration['achievement_level'] = so_line.achievement_level
	# 	return