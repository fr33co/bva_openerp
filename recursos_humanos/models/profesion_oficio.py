# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Tipo_grado(osv.Model):
	_name="hr.level.instruction"

	_order = 'tipo'
	
	_rec_name = 'tipo'
	
	_columns = {

		'tipo': fields.char(string = "Grado", size = 256, required = True),
	}

	_defaults = {
		#'codigo' : 
	}



