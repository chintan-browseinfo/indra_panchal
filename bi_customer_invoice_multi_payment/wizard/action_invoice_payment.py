# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

MAP_INVOICE_TYPE_PARTNER_TYPE = {
	'out_invoice': 'customer',
	'out_refund': 'customer',
	'in_invoice': 'supplier',
	'in_refund': 'supplier',
}
# Since invoice amounts are unsigned, this is how we know if money comes in or goes out
MAP_INVOICE_TYPE_PAYMENT_SIGN = {
	'out_invoice': 1,
	'in_refund': 1,
	'in_invoice': -1,
	'out_refund': -1,
}

class MultiInvoicePayment(models.TransientModel):
	_name="customer.multi.payments"
	_inherit = 'account.register.payments'

	memo = fields.Char(string='Memo')
	final_amount = fields.Float(string='Total Amount', \
		compute='_final_amount',store=True)
	customer_invoice_ids = fields.One2many('customer.invoice.lines','customer_wizard_id')
	
	@api.depends("customer_invoice_ids")
	def _final_amount(self):
		for amount in self:
			total = 0
			for i in amount.customer_invoice_ids:
				total += i.amount_to_pay
			amount.final_amount = total
	
	@api.onchange('payment_type')
	def _onchange_payment_type(self):
		if self.payment_type:
			return {'domain': {'payment_method_id': [('payment_type', '=', self.payment_type)]}}

	def _get_invoices(self):
		return self.env['account.invoice'].browse(self._context.get('active_ids',[]))

	@api.model
	def default_get(self, fields):
		context = dict(self._context or {})
		active_model = context.get('active_model')
		active_ids = context.get('active_ids')
		invoices = self.env[active_model].browse(active_ids)
	
		if any(invoice.state != 'open' for invoice in invoices):
			raise UserError(_("You can only register payments for open"
							  " invoices"))

		if any(MAP_INVOICE_TYPE_PARTNER_TYPE[inv.type] == 'supplier'
				for inv in invoices):
			raise UserError(_("You cannot pay vendor invoices "))

		if any(MAP_INVOICE_TYPE_PARTNER_TYPE[inv.type] != MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type]
			   for inv in invoices):
			raise UserError(_("You cannot mix customer invoices and vendor"
							  " bills in a single payment."))
			
		if any(inv.currency_id != invoices[0].currency_id for inv in invoices):
			raise UserError(_("In order to pay multiple invoices at once, they"
							  " must use the same currency."))

		rec = {}
		inv_list = []

		if MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type] == 'customer':
			for inv in invoices:
				inv_list.append((0,0,{
					'invoice_id' : inv.id,	
					'partner_id' : inv.partner_id.id,
					'total_amount' : inv.amount_total or 0.0,
					'payment_diff' : inv.residual or 0.0,
					'amount_to_pay' : 0.0,
					}))
			rec.update({'customer_invoice_ids':inv_list})
			
		total_amount = sum(inv.residual * MAP_INVOICE_TYPE_PAYMENT_SIGN[inv.type] for inv in invoices)
		communication = ' '.join([ref for ref in invoices.mapped('reference') if ref])
		rec.update({
			'amount': abs(total_amount),
			'currency_id': invoices[0].currency_id.id,
			'payment_type': total_amount > 0 and 'inbound' or 'outbound',
			'partner_id': invoices[0].commercial_partner_id.id,
			'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
			'communication' : communication
		})
		return rec

	def get_new_payment_vals(self,payment=None):
		""" Hook for extension """
		if payment:
			res = {
					'journal_id': self.journal_id.id,
					'payment_method_id': self.payment_method_id.id,
					'payment_date': self.payment_date,
					'communication': self.communication,
					'invoice_ids': [(4, int(inv) , None) for inv in list(payment['inv_val'])],
					'payment_type': self.payment_type,
					'amount': payment['final_total'],
					'currency_id': self.currency_id.id,
					'partner_id': int(payment['partner_id']),
					'partner_type': self.partner_type,
				}
			return res 
	
	@api.multi
	def register_multi_payment(self):
		if self.customer_invoice_ids:
			for amount in self.customer_invoice_ids:
				if not amount.amount_to_pay > 0.0:
					raise UserError(_("Amount must be strictly positive \n"
									"Enter Receive amount"))
		if not self.customer_invoice_ids:
			raise UserError(_("No invoie lines are there.\n"
									"Click on cancle button."))

		res = self.env['account.invoice'].browse(self._context.get('active_ids',[]))
		data = {}
		context = {}
		for inv in self.customer_invoice_ids:
			inv.payment_diff = inv.total_amount - inv.amount_to_pay
			partner_id = str(inv.invoice_id.partner_id.id)
			if partner_id in data:
				old_payment = data[partner_id]['final_total']
				final_total = old_payment + inv.amount_to_pay
				data[partner_id].update({
							'partner_id': partner_id,
							'final_total' : final_total,
							'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[inv.invoice_id.type],
							'payment_method_id': inv.payment_method_id
							})
				data[partner_id]['inv_val'].update({
					str(inv.invoice_id.id) :{
					'amount_to_pay' : inv.amount_to_pay,
					'payment_diff' : inv.payment_diff,
					}})
			else:
				data.update({ partner_id : {
					'invoice_id' : inv.id,
					'partner_id' : inv.partner_id.id,
					'total_amount' : inv.total_amount,
					'final_total' : inv.amount_to_pay,
					'inv_val' : { inv.invoice_id.id : {
						'amount_to_pay' : inv.amount_to_pay,
						'payment_diff' : inv.payment_diff,
						}}
					}})
		
		context.update({'payment':data})
		for payment in list(data):
			payment_ids = self.env['account.payment'].with_context(context).create(self.get_new_payment_vals(payment=data[payment]))
			payment_ids.post()	
		return {'type': 'ir.actions.act_window_close'}
	
class InvoiceLines(models.TransientModel):
	_name = 'customer.invoice.lines'

	customer_wizard_id = fields.Many2one('account.multi.payments')
	invoice_id = fields.Many2one('account.invoice',required=True,
		string="Invoice Numbers")
	partner_id = fields.Many2one('res.partner',string='Customer',
		related='invoice_id.partner_id', 
		store=True, readonly=True, related_sudo=False)
	payment_method_id = fields.Many2one('account.payment.method',string='Payment Type')
	total_amount = fields.Float("Invoice Amount", required=True)
	amount_to_pay = fields.Float(string='Receive Amount')
	payment_diff = fields.Float(string='Residual Amount',store=True,readonly=True)