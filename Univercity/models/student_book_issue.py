from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StudentApplication(models.Model):
	_name = "book.issue.module"
	_description = "Student application Module"

	student_name_id = fields.Many2one("studentinquiry.module",required=True)
	name = fields.Char(store=True, related="student_name_id.name")
	contact = fields.Char(store=True, related="student_name_id.contact")
	qualification_id = fields.Many2one("qualification.module",String="Qualification",related="student_name_id.qualification_id")
	education_id = fields.Many2one("education.module",String="Education Stream",related="qualification_id.education_id")
	course_id = fields.Many2one("univercitycourse.module")
	course_name = fields.Char(store=True,related="course_id.course_name")
	issued_book_ids = fields.One2many('library.module','book_id',String="Book Name",index=True,Store=True)
	rent_book_ids = fields.One2many('library.module','rent_book_id',String="Rent Books",index=True)
	book_type = fields.Selection((
		('rent','Rentable'),
		('sold','Saleable'),),String='Rent / Sale')
	amount_total = fields.Integer(String='Total Bill')


	@api.multi
	@api.onchange('book_type')
	def _onchange_book_type(self):
		d = {}
		for book in self:
			if book.book_type == 'sold':
				res = self.env['book.module'].search([('book_type','=','sold')])
				print "=====================res1==============",res
				d['domain'] = {'issued_book_ids.name_id':[('name_id','=',[i.name for i in res])]}
				print "d========================d1====================d",d
				return d
			if book.book_type == 'rent':
				res = self.env['book.module'].search([('book_type','=','rent')])
				print "=====================res2==============",res
				d['domain'] = {'rent_book_ids.name_id':[('name_id','=',[i.name for i in res])]}
				print "d========================d2================",d
				return d