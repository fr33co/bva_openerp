# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Solicitudes(osv.Model):
	
	'''Herenciando a hr.payslip (Nomina de Becado)'''
	
	_inherit = 'hr.applicant'
	
	_columns = {
		'cedula' : fields.char(string="Cédula", size = 8, required=True),
		'direccion_trabajo' : fields.text(string="Dirección", size = 256, required=True),
		'ano_experiencia' : fields.char(string="Año de experiencia", required=False),
	}
