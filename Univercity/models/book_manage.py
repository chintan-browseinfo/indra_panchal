from odoo import fields ,models ,api ,_

class LibraryManagement(models.Model):
	_name = 'book.module'

	name = fields.Char(string='Book name',required=True,index=True)
	book_author = fields.Char(string='Book Author',required=True)
	book_publication = fields.Char(string='Book Publication')
	book_price = fields.Float(string='Book Price')
	book_quantity = fields.Integer(string='Available books')
	book_availability = fields.Boolean(string='Availability of book')
	sequence_book_id = fields.Char(string='Book Sequence',index=True,readonly=True)
	rent_of_book = fields.Integer(string='Book Rent')
	library_book_ids = fields.Many2many('univercitycourse.module',string='Course Name')
	edu_library_book_ids = fields.Many2many('education.module',string='Education Stream')
	# remaining_books = fields.Integer(string='Available Books')
	

	@api.model
	def create(self,vals):
		seq = self.env['ir.sequence'].next_by_code('hr.book.employee') or '/'
		vals['sequence_book_id'] = seq
		return super(LibraryManagement, self).create(vals)