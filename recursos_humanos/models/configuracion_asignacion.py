# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Grado(osv.Model):
	_name="hr.config.asignacion"

	_order = 'grado_instruc'
	
	_rec_name = 'grado_instruc'

	_columns = {
		'grado_instruc': fields.char(string = "Grado de Instrucción", size = 150, required = True),
	}


