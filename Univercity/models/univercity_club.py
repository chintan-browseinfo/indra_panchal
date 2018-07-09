from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class UnivercityClub(models.Model):
	_name = "univercityclub.module"

	name = fields.Char(String="univercityclub",required=True)
	univercity_club_ids = fields.Many2many("studentapplication.module", "stu_uniclub_rel", "uniclub_id", "student_club_id",String="Club")
	club_fees = fields.Integer(String="Club Fees")
	club_duration = fields.Selection([
		("1","1 month"),
		("2","2 month"),
		("3","3 month"),
		("4","4 month"),
		("5","5 month"),
		("6","6 month"),
		("7","1 year")],String="Club Duration", required=True)	

	@api.model
	def create(self,vals):
		print "===========================vals==================",vals
		
		club = self.env["univercityclub.module"].browse(vals.get("club_fees"))
		if club:
			if vals.get("club_fees") >= 25000:
				raise ValidationError("Club is fees limit is 25k")

		create_club = super(UnivercityClub,self).create(vals)
		return create_club

	@api.multi
	def write(self,vals):
		print "===========================vals==================",vals
		
		club = self.env["univercityclub.module"].browse(vals.get("club_fees"))
		if club:
			if vals.get("club_fees") >= 25000:
				raise ValidationError("Club is fees limit is 25k")

		write_club = super(UnivercityClub,self).write(vals)
		return write_club
