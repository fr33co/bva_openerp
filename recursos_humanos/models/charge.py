# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import fields, osv

class Cargo_empleado(osv.Model):

	'''Herenciando a hr.job (Cargo)'''

	_inherit = 'hr.job'

	_order = 'cod'

	_columns = {
		'cod' : fields.char(string="Código", size = 20),
		'nivel' : fields.selection((('1','Alto nivel'),('2','Empleado'),('3','Obrero')), "Nivel", required=False),
		'asignacion' : fields.char(string="Asignacion", size = 20),
		'grado' : fields.many2one("hr.config.asignacion", "Grado de instrucción", required = False),

	}

	_defaults = {
		# 'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al espa?ol
	}


