from odoo import models, fields, api, _

class Education_field(models.Model):
	_name = 'education.module'

	name = fields.Char(String='Education Stream')
	Edu_stream = fields.Selection([('1','Science'),('2','commerce'),('3','arts')],required=True)
	Qualification = fields.Selection([('Yes',"Educated"),('No',"Abhan")])
	type = fields.Selection([
            ('bachelor', 'Bachelor'),
            ('master', 'Master'),
            ],required=True)