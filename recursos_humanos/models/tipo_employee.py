# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Res_partner_bank(osv.Model):
	
	_inherit = 'res.partner.bank'
	
	_columns = {
		'employee_name': fields.char(string = "Empleado", size = 150, required = True),
	}
