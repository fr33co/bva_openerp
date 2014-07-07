# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Seguridad(osv.Model):
	
	'''Herenciando a hr.holidays (Nomina de Empleado)'''
	
	_inherit = 'hr.holidays'
	
	_columns = {
		'fecha_actual' : fields.char(string="Fecha de registro", size = 50, readonly=True),
		
	}

	_defaults = {
		'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español
	}
	
	
