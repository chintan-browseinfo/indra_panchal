from odoo import fields ,models ,api ,_

class LibraryManagement(models.Model):
	_name = "book.module"

	name = fields.Char(String="Book name",required=True,index=True)
	book_author = fields.Char(String="Book Author",required=True)
	book_publication = fields.Char(String="Book Publication")
	book_price = fields.Float(String="Book Price")
	book_quantity = fields.Integer(String="Available books")
	book_availability = fields.Boolean(String="Availability of book")
	book_sold = fields.Boolean(String="Book for Sale")
	book_type = fields.Selection((
		('rent','Rentable'),
		('sold','Saleable'),),String='Rent / Sale')
	sequence_book_id = fields.Char(String="Book Sequence",index=True,readonly=True)
	rent_of_book = fields.Integer(String='Book Rent')
	library_book_ids = fields.Many2many("univercitycourse.module","library_univercity_rel","library_book_id","univercity_book_id",String="Course Name")
	# remaining_books = fields.Integer(String="Available Books")
	edu_library_book_ids = fields.Many2many("education.module","edu_library_rel","library_edu_id","edu_library_id",String="Education Stream")

	@api.model
	def create(self,vals):
		seq = self.env['ir.sequence'].next_by_code('hr.book.employee') or '/'
		vals['sequence_book_id'] = seq
		return super(LibraryManagement, self).create(vals)
	# @api.multi
	# @api.onchange('book_type')
		# def _onchange_book_type(self):
			

	