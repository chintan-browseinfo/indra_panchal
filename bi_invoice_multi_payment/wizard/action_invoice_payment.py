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
	_name="account.multi.payments"
	_inherit = 'account.register.payments'

	payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money')], string='Payment Type', required=True)
	partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')])
	journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('type', 'in', ('bank', 'cash'))])
	payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
	memo = fields.Char(string='Memo')
	final_amount = fields.Float(string='Total Receivable Amount',compute='_final_amount',store=True)
	payment_invoice_ids = fields.One2many('invoice.lines','wizard_id')

	@api.depends("payment_invoice_ids",'final_amount')
	def _final_amount(self):
		for amount in self:
			total = 0
			for i in amount.payment_invoice_ids:
				print "i...........---------------------",i
				total += i.amount_to_pay
				print "total-----------------------------",total
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
		
		invoices = self.env[active_model].browse(active_ids)
		if any(invoice.state != 'open' for invoice in invoices):
			raise UserError(_("You can only register payments for open"
							  " invoices"))
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
					'total_amount' : inv.residual or 0.0,
					'amount_to_pay' : 0.0,
					'payment_diff' : inv.residual or 0.0,
					}))
			rec.update({'payment_invoice_ids':inv_list})
		
		total_amount = sum(inv.residual * MAP_INVOICE_TYPE_PAYMENT_SIGN[inv.type] for inv in invoices)
		communication = ' '.join([ref for ref in invoices.mapped('reference') if ref])
		print "total_amount=========================",total_amount
		print "communication-------------------------------",communication
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
					'amount': payment['total_amount'],
					'currency_id': self.currency_id.id,
					'partner_id': int(payment['partner_id']),
					'partner_type': self.partner_type,
				}
			print "res---------------------------------",res
			return res 
	
	@api.multi
	def register_multi_payment(self):
		if not self.payment_invoice_ids:
			raise UserError(_("No invoice line's are there"))
		res = self.env['account.invoice'].browse(self._context.get('active_ids',[]))
		print "res11-------------------------------------",res
		data = {}
		context = {}
		
		for inv in self.payment_invoice_ids:
			inv.payment_diff = inv.total_amount - inv.amount_to_pay
			print "inv.payment_diff--------------------",inv.payment_diff
			partner_id = str(inv.invoice_id.partner_id.id)
			print "partner_id-------------------------------",partner_id
			if partner_id in data:
				data[partner_id].update({
							'partner_id': partner_id,
							'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[inv.invoice_id.type],
							'payment_method_id': inv.payment_method_id
							})
				print "data1-----------------------------------",data
				data[partner_id]['inv_val'].update({
					str(inv.invoice_id.id) :{
					'amount_to_pay' : inv.amount_to_pay,
					'payment_diff' : inv.payment_diff,
					}})
				print "data2-----------------------------------",data
			else:
				data.update({ partner_id : {
					'invoice_id' : inv.id,
					'partner_id' : inv.partner_id.id,
					'total_amount' : inv.total_amount,
					'amount_to_pay': inv.amount_to_pay,
					'inv_val' : { inv.invoice_id.id : {
						'amount_to_pay' : inv.amount_to_pay,
						'payment_diff' : inv.payment_diff,
						}}
					}})
			print "data-----------------------------------",data
		context.update({'payment':data})
		print 'context=====-----------------------------------',context
		for p in list(data):
			payment = self.env['account.payment'].with_context(context).create(self.get_new_payment_vals(payment=data[p]))
			print "payment---------------------------------",payment
			payment.post()
	
		return {'type': 'ir.actions.act_window_close'}
	
class InvoiceLines(models.TransientModel):
	_name = 'invoice.lines'

	wizard_id = fields.Many2one('account.multi.payments')
	invoice_id = fields.Many2one('account.invoice',string='Invoice',required=True)
	partner_id = fields.Many2one('res.partner',string='Partner',store=True)
	payment_method_id = fields.Many2one('account.payment.method',string='Payment Type')
	total_amount = fields.Float("Invoice Amount", required=True)
	amount_to_pay = fields.Float(string='Receive Amount')
	payment_diff = fields.Float(string='Remaining amount',store=True,readonly=True)

	@api.onchange('amount_to_pay')
	def _pay_difference(self):
		self.payment_diff = self.total_amount - self.amount_to_pay
