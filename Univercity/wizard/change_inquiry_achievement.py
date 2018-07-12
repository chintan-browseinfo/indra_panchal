import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class ChangeAchievement(models.TransientModel):
	_name = 'change.inquiry.achievement'
	_description = 'Change Achievement'

	change_achievement_ids = fields.One2many('changeachievement.module','editor_id',String="Achievement")

	@api.model
	def default_get(self, default_fields):
		res = super(ChangeAchievement, self).default_get(default_fields)
		change_achieve = self.env['studentinquiry.module'].browse(self._context.get('active_id'))
		val = []
		for i in change_achieve.achievement_ids:
			print "'''i=============================",i
			val.append({
				'achievement_id' : i.achievement_id.id,
				'name' : i.name,
				'achievement_level' : i.achievement_level,
				})

		res['change_achievement_ids'] = val	
		res = self._convert_to_write(res)
		return res

	@api.multi
	def change_inquiry_achievement(self):
		self.ensure_one()
		for achive in self.change_achievement_ids:
			values = achive.get_registration_data()
			print "===============values=============",values
			if achive:
				achive.write(values)
				print "===============values=============",achive
			else:
				self.env['studentinquiry.module'].create(values)		
		if self.env.context.get('active_model') == 'studentinquiry.module':
			for order in self.env['studentinquiry.module'].browse(self.env.context.get('active_ids', [])):
				order.achievement_ids._update_value(confirm=True)		
		return
		
		

class ChangeInquiryAchievement(models.TransientModel):
	_name = 'changeachievement.module'

	editor_id = fields.Many2one('change.inquiry.achievement')	
	achievement_id = fields.Many2one('studentinquiry.module')
	name = fields.Char(String='Name of Achievemnet')
	achievement_level = fields.Selection((('taluka','taluka'),
		('jila','jila'),
		('state','state'),
		('national','national'),
		('international','international')),String="Achievement Level")

	@api.multi
	def get_registration_data(self):
		self.ensure_one()
		return {
			'editor_id':self.editor_id.id,
			'achievement_id':self.achievement_id.id,
			'name' : self.name,
			'achievement_level' : self.achievement_level,
		}


	# @api.multi
	# def _update_val(self):
	# 	Reg = self.env['change.inquiry.achievement'].browse(self._context.get('active_id'))
	# 	print "Reg====================================",Reg
	# 	for so_line in self.filtered('editor_id'):
	# 		print "so_line=====================",so_line,so_line.name,so_line.achievement_level	
	# 		registration = {}
	# 		# registration['achievement_id'] = so_line.achievement_id
	# 		registration['name'] = so_line.name
	# 		registration['achievement_level'] = so_line.achievement_level
	# 	return