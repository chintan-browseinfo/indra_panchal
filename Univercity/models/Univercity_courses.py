from odoo import api, fields, models, _

class UnivercityCourses(models.Model):
	_name = "univercitycourse.module"
	_description = "Univercity Courses Module"

	name = fields.Char(string='Course', required=True, copy=False)
	education_id = fields.Many2one('education.module',String="Education Stream")
	sub_education_id = fields.Many2one('subeducation.module',String="Sub Education Stream")
	course_name = fields.Char(String='Course Name',required=True)
	course_duration = fields.Char(String='Course Duration',required=True)
	course_fees = fields.Char(String='Course Fees',required=True,default=None,size=30)
	course_time = fields.Selection([
		('F','Full Time'),
		('H','Part Time')],String='Course Time',required=True)

	# student_ids = fields.Many2many('studentapplication.module', 'stu_course_rel', 'student_id', 'course_id', string="Course")