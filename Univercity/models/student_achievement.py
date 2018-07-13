from odoo import models, api, fields, _
from datetime import datetime, timedelta

class StudentInquiry(models.Model):
	_name="studentachievement.module"

	name = fields.Char(String='Competition Name')
	achievement_id =  fields.Many2one('studentinquiry.module',String="Achievement List")
	sports_name = fields.Selection((('Kho-Kho','Kho-Kho'),
		('Kabbadi','Kabbadi'),
		('Football','Football'),
		('Cricket','Cricket'),
		('Chess','Chess'),
		('Hockey','Hockey')),String="Sports Name")
	sport_achievement = fields.Selection((('district','District'),
		('domestic','Domestic'),
		('national','National'),
		('international','International')),String="Sports achievement level")