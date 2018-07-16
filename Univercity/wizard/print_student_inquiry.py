import time
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class printreport(models.TransientModel):
	_name = 'print.module'
	
	student_id = fields.Many2one("studentinquiry.module")
	name = fields.Char()
	contact = fields.Char()
	email = fields.Char()
	qualification_id = fields.Many2one('qualification.module',String="Qualification")

	@api.multi
	def check_report(self):
		data = {}
		data['form'] = self.read(['student_id','name', 'email', 'contact','qualification_id'])[0]
		return self._print_report(data)

	def _print_report(self, data):
		data['form'].update(self.read(['student_id', 'name', 'email', 'contact','qualification_id'])[0])
		return self.env['report'].get_action(self, 'sales_report.report_salesperson', data=data)

	@api.model
	def render_html(self, docids, data=None):
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_id'))
		sales_records = []
		orders = self.env['studentapplication.module'].search([('student_id', '=', docs.student_id.id)])
		if docs.date_from and docs.date_to:
			for order in orders:
				if parse(docs.date_from) <= parse(order.date_order) and parse(docs.date_to) >= parse(order.date_order):
					sales_records.append(order);
				else:
					raise UserError("Please enter duration")

		docargs = {
		'doc_ids': self.ids,
		'doc_model': self.model,
		'docs': docs,
		'time': time,
		'orders': sales_records
		}
		return self.env['report'].render('sales_report.report_salesperson', docargs)	