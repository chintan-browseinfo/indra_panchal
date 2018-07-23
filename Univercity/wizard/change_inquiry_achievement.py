import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class ChangeAchievement(models.TransientModel):
	_name = 'change.inquiry.achievement'
	_description = 'Change Achievement'

	change_achievement_ids = fields.One2many('changeachievement.module','editor_id')

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
				'sports_name' : i.sports_name,
				'sport_achievement' : i.sport_achievement,
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
			reg = self.env['studentinquiry.module'].browse(self.env.context.get('active_ids', []))
			value=[]
			val=[]
			for i in reg.achievement_ids:
				val.append(i.id)
			k=0
			for j in self.change_achievement_ids:
				if k>=len(val):
					value.append([0,0,{
						'name' : j.name,
						'sports_name' : j.sports_name,
						'sport_achievement' : j.sport_achievement,}
						])
				else:
					print"========jjjjjjjjjjjjjjjjj==========",j.name
					value.append([1,val[k],{
						'name':j.name,
						'sports_name' : j.sports_name,
						'sport_achievement':j.sport_achievement,}])
				k=k+1	
			print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",value
			reg.achievement_ids = value
		return


class ChangeInquiryAchievement(models.TransientModel):
	_name = 'changeachievement.module'

	editor_id = fields.Many2one('change.inquiry.achievement')	
	achievement_id = fields.Many2one('studentinquiry.module')
	name = fields.Char(string='Competition Name')
	sports_name = fields.Selection((('Kho-Kho','Kho-Kho'),
		('Kabbadi','Kabbadi'),
		('Football','Football'),
		('Cricket','Cricket'),
		('Chess','Chess'),
		('Hockey','Hockey')),string="Sports Name")
	sport_achievement = fields.Selection((('district','District'),
		('domestic','Domestic'),
		('national','National'),
		('international','International')),string="Sports achievement level")

	@api.multi
	def get_registration_data(self):
		self.ensure_one()
		return {
			'editor_id':self.editor_id.id,
			'achievement_id':self.achievement_id.id,
			'name' : self.name,
			'sports_name' : self.sports_name,
			'sport_achievement' : self.sport_achievement,
		}