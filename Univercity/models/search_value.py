from odoo import models, fields, api, _
from odoo.osv import expression

class SearchByNumber(models.Model):
	_inherit= 'res.partner'

	@api.model
	def name_search(self, name='', args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('display_name', '=ilike', name + '%'),'|', ('phone', operator, name), ('mobile',operator,name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&', '!'] + domain[1:]
		value  = self.search(domain + args, limit=limit)
		return value.name_get()
		res = super(SearchByNumber, self).name_search()

	@api.multi
	@api.depends('name','country_id','lang')
	def name_get(self):
		res = super(SearchByNumber, self).name_get()
		result = []
		for partner in self:
			value = partner.name + ' ' + str(partner.country_id.name) + ' ' + str(partner.lang)
			print ("============name===================",value)
			result.append((partner.id,value))
			print ("============result===================",result)
		return result
		res = super(SearchByNumber, self).name_search()