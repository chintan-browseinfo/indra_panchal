from odoo import models, fields, api, _

class UnivercityClub(models.Model):
	_name = 'univercityclub.module'

	name = fields.Char(String='univercityclub',required=True)
	univercity_club_ids = fields.Many2many('studentapplication.module', 'stu_uniclub_rel', 'uniclub_id', 'student_club_id',  string="Club")
	club_fees = fields.Integer(String='Club Fees')
	club_duration = fields.Selection([
		('1','1 month'),
		('2','2 month'),
		('3','3 month'),
		('4','4 month'),
		('5','5 month'),
		('6','6 month'),
		('7','1 year')],String="Club Duration", required=True)	

	@api.model
	def create(self,vals):
		print '===========================vals==================',vals
		
		club = self.env['univercityclub.module'].browse(vals.get('club_fees'))

		create_club = super(UnivercityClub,self).create(vals)
		return create_club