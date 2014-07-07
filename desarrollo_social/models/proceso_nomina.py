# -*- coding: utf-8 -*-
import time # Necesario para las funciones de Fecha

from datetime import date
from openerp.osv import fields, osv

class ProcesoNomina(osv.Model):
	
	'''Herenciando a hr.payslip.run (Procesamiento de nóminas)'''
	
	_inherit = 'hr.payslip.run'
	
	_columns = {
		'fecha' : fields.char(string="Fecha actual",readonly=True),
	}
	
	_defaults = {
		'fecha': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español

	}

