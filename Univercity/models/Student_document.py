from odoo import models, fields, api, _

class Univercity_club(models.Model):
	_name = 'studentdocument.module'

	name = fields.Char(String='univercityclub',required=True)
	student_id = fields.Many2one('studentapplication.module',readonly=True String='Student')
	document_name = fields.Char(related='student_id.name', store=True)
