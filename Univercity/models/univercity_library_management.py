from odoo import fields ,models ,api ,_
from datetime import datetime, timedelta

class LibraryManagement(models.Model):
	_name = "library.module"

	name_id = fields.Many2one('book.module',string="Book name",required=True,index=True)
	name = fields.Char(string="Book name",related="name_id.name")
	rent_book_id = fields.Many2one('book.issue.module', string="Book Rent")
	book_author = fields.Char(string="Book Author",required=True,related="name_id.book_author")
	book_publication = fields.Char(string="Book Publication",related="name_id.book_publication")
	book_availability = fields.Boolean(string="Availability of Book",related="name_id.book_availability")
	book_price = fields.Float(string="Book Price",related="name_id.book_price")
	book_quantity = fields.Integer(string="Available books",related="name_id.book_quantity")
	purchase_quantity = fields.Integer(string="Purchase Quantity",default=1)	
	issue_date = fields.Date(string="Issue Date",required=True, copy=False,default=fields.Datetime.now)
	return_date = fields.Date(string="Return Date", copy=False,default=fields.Datetime.now)
	rent_of_book = fields.Integer(string='Book Rent',store=True,related="name_id.rent_of_book")
	rent_amount = fields.Integer(string="Rent Amount",compute="_total_rent")
	

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
			if rent.return_date:	
				today = datetime.today().date()
				d1=datetime.strptime(rent.return_date,"%Y-%m-%d").date()
				days = abs((d1-today).days)
				amount = days * rent.rent_of_book
				rent.rent_amount = amount
