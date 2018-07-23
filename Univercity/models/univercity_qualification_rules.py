from odoo import models, api, fields, _

class StudentQualification(models.Model):
	_name="qualification.module"

	name = fields.Char(Strong="Qualification Name",required=True)
	education_id = fields.Many2one("education.module",string="Education Stream")