# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Propietario(osv.Model):
	_name="hr.propietario"

	_order = 'codigo asc'
	
	_rec_name = 'codigo'

	_columns = {
		'codigo': fields.char(string = "Código", size = 10, required = True),
		'propietario': fields.text(string = "Propietario", size = 256, required = True),
		'cuenta': fields.char(string = "Cuenta", size = 200, required = False),
		'estandar' : fields.char(string = "Estandar", size = 200, required = False),

	}

	_defaults = {
		#'codigo' : 
	}



