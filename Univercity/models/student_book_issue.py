from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StudentApplication(models.Model):
	_name = "book.issue.module"
	_description = "Student application Module"

	student_name_id = fields.Many2one("studentinquiry.module",required=True)
	name = fields.Char(store=True, related="student_name_id.name")
	contact = fields.Char(store=True, related="student_name_id.contact")
	qualification_id = fields.Many2one("qualification.module",string="Qualification",related="student_name_id.qualification_id")
	education_id = fields.Many2one("education.module",string="Education Stream",related="qualification_id.education_id")
	course_id = fields.Many2one("univercitycourse.module")
	course_name = fields.Char(store=True,related="course_id.course_name")
	rent_book_ids = fields.One2many('library.module','rent_book_id',index=True)
	rent_total = fields.Integer(string='Total Rent',readonly=True,compute='_onchange_rent')
	
	@api.multi
	@api.onchange('rent_book_ids')
	def _onchange_rent(self):
		rent = 0	
		for book in self:
			for i in book.rent_book_ids:
				rent += i.rent_amount
				print "total====================================",rent
			book.update({'rent_total' : rent})

