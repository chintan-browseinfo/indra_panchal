from odoo import fields ,models ,api ,_

class LibraryManagement(models.Model):
	_name = "library.module"

	name = fields.Char(String="Book name",required=True,index=True)
	book_author = fields.Char(String="Book Author",required=True)
	book_publication = fields.Char(String="Book Publication")
	book_price = fields.Char(String="Book Price")
	book_availability = fields.Boolean(String="Availability of Book")
	book_quantity = fields.Char(String="Available books")
	library_book_ids = fields.Many2many("univercitycourse.module","library_univercity_rel","library_book_id","univercity_book_id",String="Course Name")
	edu_library_book_ids = fields.Many2many("education.module","edu_library_rel","library_edu_id","edu_library_id",String="Education Stream")