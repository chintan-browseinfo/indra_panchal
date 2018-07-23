from odoo import models, fields, api, _

class Education_field(models.Model):
	_name = "education.module"

	name = fields.Char(string="Education Stream")
	library_edu_book_ids = fields.Many2many("book.module","edu_library_rel","edu_library_id","library_edu_id",string="Book Name")