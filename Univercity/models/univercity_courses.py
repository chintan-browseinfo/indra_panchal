from odoo import api, fields, models, _
from odoo.osv import expression

class UnivercityCourses(models.Model):
	_name = "univercitycourse.module"
	_description = "Univercity Courses Module"

	name = fields.Char(string="Course", required=True, copy=False)
	code = fields.Char(string="Course Code",required=True, copy=False)
	education_id = fields.Many2one("education.module",String="Education Stream")	
	course_type = fields.Selection([("Bachelor","Bachelor Degree"),
		("Master","Master Degree"),
		("Diploma","Diploma Degree")],index=True,String="Degree Type")
	course_name = fields.Char(String="Course Name",required=True)
	qualification_id = fields.Many2one("qualification.module",String="Qualification")
	course_duration = fields.Selection((("0","6 month"),
		("1","1 year"),
		("2","2 years"),
		("3","3 years"),
		("4","4 years"),
		("5","5 years")),String="Course Duration",required=True)
	course_fees = fields.Char(String="Course Fees",required=True,default=None,size=30)
	course_time = fields.Selection((("Full Time","Full Time"),
		("Part Time","Part Time")),String="Course Time",required=True)
	
	univercity_book_ids = fields.Many2many("library.module","library_univercity_rel","univercity_book_id","library_book_id",String="Book Name")		
	@api.model
	def name_search(self, name="", args=None, operator="ilike", limit=100):
		args = args or []
		domain = []
		if name:
			domain = ["|", ("name", "=ilike", name + "%"), ("code",operator,name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ["&", "!"] + domain[1:]
		res = super(UnivercityCourses, self).search(domain + args, limit=limit).name_get()
		return res

	@api.model
	@api.depends("name","code")
	def name_get(self):
		result = []
		for course in self:
			course_result = course.code + " | " + course.name
			# print ("============name===================",course_result)
			result.append((course.id,course_result))
			# print ("============result===================",result)
		return result
