# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Grado(osv.Model):
	_name="hr.degree"

	_order = 'grado'
	
	_rec_name = 'grado'
	
	_columns = {

		'grado': fields.char(string = "Grado", size = 256, required = True),
		'tipo' : fields.many2one('hr.level.instruction','Tipo',required=False),
	}

	_defaults = {
		#'codigo' : 
	}



