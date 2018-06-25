from odoo import models, fields, api, _

class Univercity_club(models.Model):
	_name = 'univercityclub.module'

	name = fields.Char(String='univercityclub',required=True)
	univercity_club_ids = fields.Many2many('studentapplication.module', 'stu_uniclub_rel', 'uniclub_id', 'student_club_id',  string="Club")
	