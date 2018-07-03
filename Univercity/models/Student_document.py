from odoo import models, fields, api, _

class StudentDocument(models.Model):
	_name = 'studentdocument.module'

	name = fields.Char(String='Student Document',required=True)
	student_doc_ids = fields.Many2many('studentapplication.module','app_doc_rel','doc_id','app_id',String='Student')
