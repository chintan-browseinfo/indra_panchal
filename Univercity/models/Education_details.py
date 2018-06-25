from odoo import models, fields, api, _

class Education_field(models.Model):
	_name = 'education.module'

	name = fields.Char(String='Education Stream',required=True)