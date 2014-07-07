# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class tipoEmpleado(osv.Model):
	_name="becados.tipoempleado"

	_order = 'tipo_emp'
	
	_rec_name = 'tipo_emp'
	
	_columns = {
		'tipo_emp': fields.char(string = "Tipo de Empleado", size = 150, required = True),
	}

