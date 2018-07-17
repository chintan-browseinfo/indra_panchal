from odoo import fields ,models ,api ,_

class LibraryManagement(models.Model):
	_name = "book.module"

	name = fields.Char(String="Book name",required=True,index=True)
	book_author = fields.Char(String="Book Author",required=True)
	book_publication = fields.Char(String="Book Publication")
	book_price = fields.Float(String="Book Price")
	book_quantity = fields.Integer(String="Available books")
	book_availability = fields.Boolean(String="Availability of Book")
	book_sold = fields.Boolean(String="Book for Sale")
	book_type = fields.Selection((
		('rent','Rentable'),
		('sold','Saleable'),),String='Rent / Sale')
	rent_of_book = fields.Integer(String='Book Rent')
	library_book_ids = fields.Many2many("univercitycourse.module","library_univercity_rel","library_book_id","univercity_book_id",String="Course Name")
	edu_library_book_ids = fields.Many2many("education.module","edu_library_rel","library_edu_id","edu_library_id",String="Education Stream")

	# @api.multi
	# @api.onchange('book_type')
		# def _onchange_book_type(self):
			
			

	