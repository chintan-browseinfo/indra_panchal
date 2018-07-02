from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StudentApplication(models.Model):
	_name = "studentapplication.module"
	_inherit = 'mail.thread'
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

		for o in self:
			o.course_time = o.course_id.course_time

	course_name = fields.Char('course_name',compute=_compute_student_code)
	course_time = fields.Char('course_time',compute=_compute_student_code)
	course_id = fields.Many2one('univercitycourse.module', String="Course")
	
	@api.one
	@api.depends('student_club_ids')
	def _cal_fees(self):
		fees_bucket = 0
		for fees in self:
			for ids in fees.student_club_ids:
				fees_bucket += ids.club_fees 

		fees.total_fees = fees_bucket
	
	student_club_ids = fields.Many2many('univercityclub.module', 'stu_uniclub_rel', 'student_club_id','uniclub_id', string="Club")
	

	@api.model
	def create(self,vals):
		print "=========vals=========",vals
		if not vals.get('student_club_ids'):
			raise ValidationError(_('Configuration error!\nYou have to participate at least 1 club.'))
		elif len(vals.get('student_club_ids')[0][2]) > 3:
			raise ValidationError(_('Configuration error!\nYou cannot participate in more than 3 clubs.'))
		club = self.env['univercitycourse.module'].browse(vals.get('course_id'))
		# print "=========clubs=========",club,vals.get('education_id'),club.education_id
		if vals.get('education_id') != club.education_id.id:
			raise ValidationError(_('Configuration error!\nYou cannot select courses from another streams.'))
		student = super(StudentApplication,self).create(vals)
	
		return student
		# if student:
		# 	email_id = self.env['studentapplication.module'].browse(vals.get('email'))
		# 	print '=====================email===========',email_id
		# if student:
		# 	mail = email_id.send_email(self.id, force_send=True)

	@api.multi
	def write(self,vals):
		# print "=========vals=========",vals
		club = self.env['univercitycourse.module'].browse(vals.get('course_id'))
		# print "=========clubs=========",club,vals.get('education_id'),club.education_id
		if vals.get('education_id') != club.education_id.id:
			raise ValidationError(_('Configuration error!\nYou cannot select courses from another streams.'))
		student = super(StudentApplication,self).write(vals)
		
		return student

	total_fees = fields.Char(String='Total Fees',compute='_cal_fees',store=True )