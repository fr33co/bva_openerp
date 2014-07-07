# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Contrato(osv.Model):
	
	'''Herenciando a hr.contract (Nomina de Becado)'''
	
	_inherit = 'hr.contract'
	
	_columns = {
		'fecha_actual' : fields.char(string="Fecha de registro", size = 8, readonly=True),
		
	}

	_defaults = {
		'fecha_actual': lambda *a: time.strftime('%d-%m-%Y'),
	}
	
	
