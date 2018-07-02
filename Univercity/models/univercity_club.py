from odoo import models, fields, api, _

class UnivercityClub(models.Model):
	_name = 'univercityclub.module'

	name = fields.Char(String='univercityclub',required=True)
	univercity_club_ids = fields.Many2many('studentapplication.module', 'stu_uniclub_rel', 'uniclub_id', 'student_club_id',  string="Club")
	club_fees = fields.Integer(String='Club Fees')
	club_duration = fields.Selection([
		('1','1 month'),
		('2','2 month'),
		('3','3 month'),
		('4','4 month'),
		('5','5 month'),
		('6','6 month'),
		('7','1 year')],String="Club Duration", required=True)	

	@api.model
	def create(self,vals):
		name = vals.get('name', self.env.user.name)
		create_club = super(UnivercityClub,self).create(vals)
		if vals.get('name', _('New')) == _('New'):
			if 'club_fees' in vals:
				if vals['club_fees'] > 50000:
					raise UserError(_('club fees must less than 70000'))
				else:
					vals['club_fees'] = self.env['ir.sequence'].next_by_code('univercityclub.module')
					vals['club_fees'] = club_fees.name
		create_club = super(UnivercityClub,self).create(vals)
		return create_club

		# club_fees = super(UnivercityClub, self.with_context(create_club_club=True)).create(vals)
  #       # When a unique variant is created from tmpl then the standard price is set by _set_standard_price
  #       if not (self.env.context.get('create_from_tmpl') and len(product.product_tmpl_id.product_variant_ids) == 1):
  #           product._set_standard_price(vals.get('standard_price') or 0.0)
  #       return product