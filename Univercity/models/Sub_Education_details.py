from odoo import models, fields, api, _

class Sub_Education_field(models.Model):
	_name = 'subeducation.module'

	name = fields.Char(String='Sub Education Stream',required=True)