import time
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class ChangeInquiryAchievement(models.TransientModel):
	_name = 'changeachievement.module'

	editor_id = fields.Many2one('change.inquiry.achievement')
	achivement_id = fields.Many2one('studentachievement.module')
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
			'achivement_id' : self.editor_id.achivement_id.id,
			'name' : self.editor_id.achivement_id.name,
			'achievement_level' : self.editor_id.achivement_id.achievement_level,
		}