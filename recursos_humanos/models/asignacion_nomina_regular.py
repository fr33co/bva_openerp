# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha
import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class Movement_payslip(osv.Model):
	_name="hr.movement.payslip"

	_order = 'asignacion' # Se orden las asignaciones del empleado
	_order = 'deduccion' # Se orden las deducciones del empleado

	_rec_name = 'cedula'

	_columns = {
		'cedula': fields.char(string = "Cédula", size = 10, required = False),
        'cod': fields.char(string = "Código", size = 10, required = False),
        'frecuencia': fields.char(string = "Frecuencia", required = False),
        'descripcion': fields.char(string = "Descripción", required = False),
        'cantidad_d': fields.char(string = "Dias", size = 10, required = False),
	'cantidad_h': fields.char(string = "Horas", size = 10, required = False),
        'asignacion': fields.char(string = "Asignaciones", size = 10, required = False),
        'deduccion': fields.char(string = "Deducciones", size = 10, required = False),
	'asig_deduc' : fields.many2one("hr.movement.employee", "Asignaciones / Deducciones", required = False),
	'filtro': fields.char(string = "", size = 10, required = False),
	'incidencia': fields.char(string = "Incidencia", size = 10, required = False),
	'tipo_nomina': fields.char(string = "Tipo nomina", size = 10, required = False),
	'item': fields.char(string = "", size = 10, required = False), # Elemento de accion
	}

	_defaults = {
		#'reingreso' : lambda *a: time.strftime("%Y-%m-%d"),
	}



