# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Sede(osv.Model):
	_name="becados.sedes"

	_order = 'sede'
	
	_rec_name = 'sede'
	
	_columns = {
		'sede': fields.char(string = "Sede", size = 150, required = True),
	}


