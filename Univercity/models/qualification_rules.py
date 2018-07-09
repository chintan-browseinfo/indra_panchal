from odoo import models, api, fields, _

class StudentQualification(models.Model):
	_name="qualification.module"

	name = fields.Char(Strong="Qualification Name",required=True)
	