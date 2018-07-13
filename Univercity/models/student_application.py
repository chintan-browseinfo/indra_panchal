from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from random import randint
import random
import string

class StudentApplication(models.Model):
	_name = "studentapplication.module"
	_inherit = "mail.mail"
	_description = "Student application Module"

	student_id = fields.Many2one("studentinquiry.module",required=True,track_visibility="onchange")
	name = fields.Char(related="student_id.name")
	contact = fields.Char(related="student_id.contact")
	email = fields.Char(related="student_id.email")
	address = fields.Text(related="student_id.address")
	birthday = fields.Date(related="student_id.birthday")
	Age =  fields.Char(related="student_id.Age")
	gender = fields.Selection(related="student_id.gender")
	qualification_id = fields.Many2one("qualification.module",String="Qualification")
	education_id = fields.Many2one("education.module",String="Education Stream")

	state = fields.Selection([
			("confirm", "confirm"),
			("login", "login"),
			("password","password"),			
			("email","SendEmail"),
			("finished","done"),
			],default="confirm")

	@api.multi
	@api.depends("course_id")
	def _compute_student_code(self):
		for o in self:
			o.course_name = o.course_id.course_name

		for o in self:
			o.course_time = o.course_id.course_time	

	course_name = fields.Char(compute="_compute_student_code")
	course_time = fields.Char(compute="_compute_student_code")
	course_id = fields.Many2one("univercitycourse.module")
	
	@api.one
	@api.depends("student_club_ids")
	def _cal_fees(self):
		
		fees_bucket = 0
		for fees in self:
			for ids in fees.student_club_ids:
				fees_bucket += ids.club_fees 

		fees.total_fees = fees_bucket

	student_club_ids = fields.Many2many("univercityclub.module", "stu_uniclub_rel", "student_club_id","uniclub_id",String="Student Club")
	total_fees = fields.Char(compute="_cal_fees",store=True )

	aadharid = fields.Boolean(String="Aadhar Card")
	aadharnumber = fields.Char(String="Aadhar Number")
	passport = fields.Boolean(String="Passport") 
	liesence = fields.Boolean(String="Liesence")

	enroll_id = fields.Char(String="Enrollment Number", index=True)
	password  = fields.Char(String="password")

	@api.multi
	def confirm_progressbar(self):
		self.write({
			"state":"login"
		})

	@api.multi
	@api.depends("enroll_id")
	def enroll_progressbar(self):
		if not self.enroll_id:
			self.write(
				{"enroll_id": "".join(random.SystemRandom().choice(string.digits) for _ in range(randint(3,9))),
				"state":"password"})

		if self.enroll_id:
			self.write({
				"state":"password"
				})

	@api.multi
	@api.depends("password")
	def password_progressbar(self):
		if not self.password:
			self.write(
				{"password": "".join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(randint(3,9))),
				"state":"finished",})
		
		if self.password:
			self.write({
				"state":"finished"})

	@api.multi
	def done_progressbar(self):
		self.write({
			"state":"confirm"
		})

	# @api.multi
	# def btn_send_email(self):
	# 	proposal_title_approved()
	
	@api.model
	def create(self,vals):
		if vals.get("student_club_ids"):
			if len(vals.get("student_club_ids")[0][2]) > 3:
				raise ValidationError(_("Configuration error!\nYou cannot participate in more than 3 clubs."))
		
		club = self.env["univercitycourse.module"].browse(vals.get("course_id"))		
		if vals.get("education_id") != club.education_id.id:
			raise ValidationError(_("Configuration error!\nYou cannot select courses from another streams."))
		
		a_id = self.env["studentapplication.module"].browse(vals.get("aadharnumber"))
		
		if False:
			return
					
		if vals.get("aadharid"):	
			# print "============aadharid====create=========",vals.get("aadharid")
			if not a_id:
				raise ValidationError(_("Configuration error!\nEnter Valid aadhar card Number \n fields Value cannot be empty"))

		if vals.get("aadharid"):
			# print "============aadharid====create=========",vals.get("aadharid")
			if a_id:
				# print "================a_id======create=======",a_id
				if not len(vals.get("aadharnumber")) == 12:
					raise ValidationError(_("Configuration error!\nEnter Valid aadhar card Number \n aadhar number must be 12 digit."))
			
		val_id = self.env["studentapplication.module"].search([("aadharnumber", "=", vals.get("aadharnumber"))])
		if vals.get("aadharid"):
			# print "============aadharid====create=========",vals.get("aadharid")
			if val_id:
				raise ValidationError(_("Configuration error!\naadhar already exists."))		

		student = super(StudentApplication,self).create(vals)
		return student
		
	@api.multi
	def write(self,vals):
		if vals.get("student_club_ids"):
			if len(vals.get("student_club_ids")[0][2]) > 3:
				raise ValidationError(_("Configuration error!\nYou cannot participate in more than 3 clubs."))
		
		club = self.env["univercitycourse.module"].browse(vals.get("course_id"))
		if vals.get("education_id"):
			if vals.get("education_id") != club.education_id.id:
				raise ValidationError(_("Configuration error!\nYou cannot select courses from another streams."))
			
		a_id = self.env["studentapplication.module"].browse(vals.get("aadharnumber"))	
		val_id = self.env["studentapplication.module"].search([("aadharnumber", "=", vals.get("aadharnumber") )])
		
		if False:
			return

		if vals.get("aadharid"):
			# print "================aadharid========write=============",vals.get("aadharid")	
			if not a_id:
				raise ValidationError(_("Configuration error!\nEnter Valid aadhar card Number \n fields Value cannot be empty"))
			
		if vals.get("aadharid"):
			if a_id:
				# print "================a_id======wirte============",a_id
				if not len(vals.get("aadharnumber")) == 12:
					raise ValidationError(_("Configuration error!\nEnter Valid aadhar card Number \n aadhar number must be 12 digit."))			
					
		if vals.get("aadharid"):
			if val_id:
				raise ValidationError(_("Configuration error!\naadhar already exists."))
	
		student = super(StudentApplication,self).write(vals)
		return student

	@api.onchange("qualification_id","education_id")
	def _course_details(self):
		res = {}
		for course in self:	
			if course.qualification_id or not course.education_id:
				res["domain"] = {"course_id":["|",("qualification_id","=",self.qualification_id.id),
				("education_id","=",self.education_id.id)]}	
			if course.qualification_id and course.education_id:
				res["domain"] = {"course_id":["&",("qualification_id","=",self.qualification_id.id),
				("education_id","=",self.education_id.id)]}
			if not course.qualification_id and not course.education_id:
				return
		return res

	# @api.multi
	# def proposal_title_approved(self):
	# 	template_obj = self.env["studentapplication.module"].sudo().search([("name","=","Create Section for Thesis")], limit=1)
	# 	body = template_obj.body_html
	# 	body=body.replace("--enrollment--",self.enroll_id)
	# 	body=body.replace("--password--",self.password)
		
	# 	if template_obj:
	# 		mail_values = {
	# 		"subject": template_obj.subject,
	# 		"body_html": body,
	# 		"email_to":";".join(map(lambda x: x, receipt_list)),
	# 		"email_cc":";".join(map(lambda x: x, email_cc)),
	# 		"email_from": template_obj.email_from,
	# 		}
	# 	create_and_send_email = self.env["mail.mail"].create(mail_values).send()       
		