# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Area(osv.Model):
	_name="becados.status"

	_order = 'status'
	
	_rec_name = 'status'
	
	_columns = {
		'status': fields.char(string = "Status", size = 150, required = True),
	}
