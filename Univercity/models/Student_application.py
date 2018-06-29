from odoo import models, fields, api, _

class StudentApplication(models.Model):
	_name = "studentapplication.module"
	_description = "Student application Module"

	name = fields.Many2one('studentinquiry.module', String='Name',required=True,track_visibility='onchange')
	contact = fields.Char(String='Contact Number',related='name.contact')
	email = fields.Char(String='Email Address',related='name.email')
	address = fields.Text(String='Address',related='name.address')
	birthday = fields.Date(string='Birthday Date',related='name.birthday')
	Age =  fields.Char('Age of Student',related='name.Age')
	gender = fields.Selection(String='select Gender',related='name.gender')
	
	education_id = fields.Many2one('education.module',String="Education")
	student_document = fields.One2many('studentdocument.module', 'student_id',String="Student Document")

	@api.multi
	@api.depends("course_id")
	def _compute_student_code(self):
		for o in self:
			o.course_name = o.course_id.course_name

	course_name = fields.Char('course_name',compute=_compute_student_code)
	course_id = fields.Many2one('univercitycourse.module', String="Course")
	# course_due = fields.Char('univercitycourse.module',related='course_id.course_time',String="Course Time")
	student_club_ids = fields.Many2many('univercityclub.module', 'stu_uniclub_rel', 'student_club_id','uniclub_id', string="Club")

	@api.one
	@api.depends('student_club_ids')
	def _cal_fees(self):
		fees_bucket = 0
		for fees in self:
			for ids in fees.student_club_ids:
				fees_bucket += ids.club_fees 
			print 'fees_bucket --->',fees_bucket 
		fees.total_fees = fees_bucket

	total_fees = fields.Char(String='Total Fees',compute='_cal_fees',store=True )
	
	# collage_club_fees = fields.Integer('univercityclub.module',related='Univercity.view_univercity_club_form',String='Total Club Fees')