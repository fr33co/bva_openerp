# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Area(osv.Model):
	_name="becados.areas"

	_order = 'area'
	
	_rec_name = 'area'
	
	_columns = {
		'area': fields.char(string = "Área", size = 150, required = True),
	}


