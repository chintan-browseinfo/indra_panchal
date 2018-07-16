from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StudentApplication(models.Model):
	_name = "book.issue.module"
	_inherit = "mail.mail"
	_description = "Student application Module"

	student_name_id = fields.Many2one("studentinquiry.module",required=True)
	name = fields.Char(store=True, related="student_name_id.name")
	contact = fields.Char(store=True, related="student_name_id.contact")
	# enroll_id = fields.Char(store=True,related="student_name_id.enroll_id")
	# password = fields.Char(store=True,related="student_name_id.password")
	qualification_id = fields.Many2one("qualification.module",String="Qualification",related="student_name_id.qualification_id")
	education_id = fields.Many2one("education.module",String="Education Stream",)
	course_id = fields.Many2one("univercitycourse.module")
	course_name = fields.Char(store=True,related="course_id.course_name")