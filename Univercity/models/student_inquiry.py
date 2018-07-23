from odoo import models, api, fields, _
from datetime import datetime, timedelta

class StudentInquiry(models.Model):
	_name="studentinquiry.module"

	@api.depends("birthday")
	def _cal_age(self):
		for ages in self:
			if not ages.birthday:
				return
			today = datetime.today().date()
			d1=datetime.strptime(ages.birthday,"%Y-%m-%d").date()
			days = abs((today - d1).days)
			years = (days // 365)
			month = ((days % 365) // 31)
			age_days = abs(((days % 365) % 30) - 7)
			ages.Age = str(years) +" years " + str(month) + " months " + str(age_days) + " days "

	name = fields.Char(string="Student Name", required=True, copy=False, index=True)
	email = fields.Char(string="Email Address",required=True,copy=False)
	contact = fields.Char(string="Contact Number",required=True,size=10,copy=False)
	address = fields.Text(string="Address")
	birthday = fields.Date(string="Birthday Date",required=True, copy=False,default=fields.Datetime.now)
	Age =  fields.Char("Age of Student", store=True, compute="_cal_age")
	aid = fields.Integer(string="ID",default=1)
	state = fields.Selection([
		("Confirm","Confirm"),
		("Cancle","Cancle")],string="state",required=True,readonly=True,copy=False,default="Confirm")
	gender = fields.Selection([
		("M","Male"),
		("F","Female")],string="select Gender",)
	qualification_id = fields.Many2one('qualification.module',string="Qualification")
	achievement_ids = fields.One2many('studentachievement.module','achievement_id')
	sequence_inq_id = fields.Char('Sequence', index=True, readonly=True)

	@api.model
	def create(self,vals):
		seq = self.env['ir.sequence'].next_by_code('hr.stu.employee') or '/'
		vals['sequence_inq_id'] = seq
		return super(StudentInquiry, self).create(vals)