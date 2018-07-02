from odoo import models, api, fields, _
from datetime import datetime, timedelta

class StudentInquiry(models.Model):
	_name="studentinquiry.module"

	@api.depends('birthday')
	def _cal_age(self):

		for ages in self:
			if not ages.birthday:
				return
			today = datetime.today().date()
			d1=datetime.strptime(ages.birthday,'%Y-%m-%d').date()
			days = abs((today - d1).days)
			years = (days // 365)
			month = ((days % 365) // 31)
			age_days = abs(((days % 365) % 30) - 7)
			ages.Age = str(years) +' years ' + str(month) + ' months ' + str(age_days) + ' days '

	name = fields.Char(String='Student Name',required=True)
	email = fields.Char(String='Email Address',required=True,copy=False)
	contact = fields.Char(String='Contact Number',required=True,size=10,copy=False)
	address = fields.Text(String='Address')
	birthday = fields.Date(string='Birthday Date',required=True, copy=False)
	Age =  fields.Char('Age of Student', store=True, compute='_cal_age')
	gender = fields.Selection([
		('M','Male'),
		('F','Female')],String='select Gender')
	qualification = fields.Selection([('ssc','10th Pass'),
		('hsc','12th Pass'),],String="Qualification") 