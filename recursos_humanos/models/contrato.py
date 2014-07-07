# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Contrato_empleado(osv.Model):
	
	'''Herenciando a hr.contract (Nomina de Empleado)'''
	
	_inherit = 'hr.contract'
	
	_columns = {
		'prueba' : fields.char(string="Prueba", size = 30, readonly=False),
		# 'fecha_actual' : fields.char(string="fecha actual", size = 30, readonly=True),
		
	}

	_defaults = {
		# 'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español
	}
	
	
