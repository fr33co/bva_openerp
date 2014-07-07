# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Alimenacion(osv.Model):
	_name = "hr.asig.alimenacion"
	
	_order = "monto"
	
	_rec_name = "monto"
	
	_columns = {
		'monto': fields.char(string="Monto / Ticket", required = False),
		'ticket': fields.char(string="Can / Ticket", required = False),
		'monto_p': fields.char(string="Monto / Pagar", required = False),
	}

