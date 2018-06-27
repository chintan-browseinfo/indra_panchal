from odoo import api, fields, models, _


class Movies(models.Model):
	_name = "movie.info"
	_description = "Movies Info"

	name = fields.Char(string='Movies Reference', required=True, copy=False)
	title = fields.Char(string='Movie Title', required=True, copy=False,)
	date_release =  fields.Date(string='Release Date', required=True, copy=False)
	account_id = fields.Many2one('res.partner', String="Producer")
	star_line = fields.One2many('star.cast', 'movie_id',String="Star KI Qatar")
	cast_ids = fields.Many2many('star.cast', 'movie_star_rel', 'movie_id', 'cast_id', string="Cast")




class StarCast(models.Model):
	_name = "star.cast"
	_description = "Star Info"

	name = fields.Char(string='Star Reference', required=True, copy=False)
	f_name = fields.Char(string='First Name', required=True, copy=False)
	m_name = fields.Char(string='Middle Name', required=True, copy=False)
	l_name = fields.Char(string='Family Name', required=True, copy=False)
	movie_id = fields.Many2one('movie.info', String="Movie")
	movie_ids = fields.Many2many('movie.info', 'movie_star_rel', 'cast_id', 'movie_id', string="Movies")
	