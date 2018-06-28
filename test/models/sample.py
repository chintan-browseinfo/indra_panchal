from odoo import api, fields, models, _
from datetime import datetime, timedelta

class Movies(models.Model):
	_name = "movie.info"
	_description = "Movies Info"

	@api.depends('date_release')
	def _cal_days(self):
		for movie in self:
			if not movie.date_release:
				return
			print "========order=============",self._context,movie.date_release
			today = datetime.today().date()
			print "========today=============",today
			d1=datetime.strptime(movie.date_release,'%Y-%m-%d').date()
			print "=====d1==========",d1
            # d2=datetime.strptime(str(today,'%Y-%m-%d')
			days = abs((today - d1).days)
			print "=====days==========",abs((today - d1).days)
			movie.days_running = days

	name = fields.Char(string='Movies Reference', required=True, copy=False)
	title = fields.Char(string='Movie Title', required=True, copy=False,)
	date_release =  fields.Date(string='Release Date', required=True, copy=False)
	partner_id = fields.Many2one('res.partner', String="Producer")
	email = fields.Many2one('account.account',related='partner_id.property_account_receivable_id', string='Account')
	star_line = fields.One2many('star.cast', 'movie_id',String="Star KI Qatar")
	cast_ids = fields.Many2many('star.cast', 'movie_star_rel', 'movie_id', 'cast_id', string="Cast")
	days_running = fields.Integer('Days', store=True, compute='_cal_days')




class StarCast(models.Model):
	_name = "star.cast"
	_description = "Star Info"

	name = fields.Char(string='Star Reference', required=True, copy=False)
	f_name = fields.Char(string='First Name', required=True, copy=False)
	m_name = fields.Char(string='Middle Name', required=True, copy=False)
	l_name = fields.Char(string='Family Name', required=True, copy=False)
	movie_id = fields.Many2one('movie.info', String="Movie")
	movie_ids = fields.Many2many('movie.info', 'movie_star_rel', 'cast_id', 'movie_id', string="Movies")
	