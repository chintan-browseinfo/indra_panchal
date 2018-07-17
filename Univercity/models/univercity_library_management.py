from odoo import fields ,models ,api ,_
from datetime import datetime, timedelta

class LibraryManagement(models.Model):
	_name = "library.module"

	name_id = fields.Many2one('book.module',String="Book name",required=True,index=True)
	name = fields.Char(String="Book name",related="name_id.name")
	book_id = fields.Many2one('book.issue.module', String="Book Issue")
	rent_book_id = fields.Many2one('book.issue.module', String="Book Rent")
	book_author = fields.Char(String="Book Author",required=True,related="name_id.book_author")
	book_publication = fields.Char(String="Book Publication",related="name_id.book_publication")
	book_availability = fields.Boolean(String="Availability of Book",related="name_id.book_availability")
	book_sold = fields.Boolean(String="Book for Sale",related="name_id.book_sold")	
	library_book_ids = fields.Many2many("univercitycourse.module","library_univercity_rel","library_book_id","univercity_book_id",String="Course Name")
	edu_library_book_ids = fields.Many2many("education.module","edu_library_rel","library_edu_id","edu_library_id",String="Education Stream")

	book_price = fields.Float(String="Book Price",related="name_id.book_price")
	book_quantity = fields.Integer(String="Available books",related="name_id.book_quantity")
	purchase_quantity = fields.Integer(String="Purchase Quantity",default=1)
	amount_bill = fields.Integer(String="Total price",compute="_bill_amount")
	
	issue_date = fields.Date(string="Issue Date",required=True, copy=False,default=fields.Datetime.now)
	return_date = fields.Date(string="Return Date",required=True, copy=False)
	rent_of_book = fields.Integer(String='Book Rent',store=True,related="name_id.rent_of_book")
	rent_amount = fields.Integer(String="Rent Amount",compute="_total_rent")
	
	@api.one
	@api.depends('book_price','purchase_quantity')
	def _bill_amount(self):
		total = 0
		for bill in self:
			if bill.book_price:
				print "=======================bill.book_price",bill.book_price
				for i in bill.book_price,bill.purchase_quantity: 
					total = (bill.book_price * bill.purchase_quantity)
					print "======================total====",total
		bill.amount_bill = total 

	@api.one
	@api.depends('return_date','rent_of_book')
	def _total_rent(self):
		for rent in self:
			if not rent.return_date:
				return
			today = datetime.today().date()
			d1=datetime.strptime(rent.return_date,"%Y-%m-%d").date()
			days = abs((d1-today).days)
			amount = days * rent.rent_of_book
			rent.rent_amount = amount