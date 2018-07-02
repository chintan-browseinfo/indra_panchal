from odoo import api, fields, models, _

class UnivercityCourses(models.Model):
	_name = "univercitycourse.module"
	_description = "Univercity Courses Module"

	name = fields.Char(string='Course', required=True, copy=False)
	education_id = fields.Many2one('education.module',String="Education Stream")	
	course_type = fields.Selection([
		('UG','Bacholer Degree'),
		('PG','Master Degree')],String='select Degree',default=None)
	course_name = fields.Char(String='Course Name',required=True)
	course_duration = fields.Selection([
		('0','6 month'),
		('1','1 year'),
		('2','2 years'),
		('3','3 years'),
		('4','4 years'),
		('5','5 years')],String='Course Duration',required=True)
	course_fees = fields.Char(String='Course Fees',required=True,default=None,size=30)
	course_time = fields.Selection([
		('F','Full Time'),
		('H','Part Time')],String='Course Time',required=True)