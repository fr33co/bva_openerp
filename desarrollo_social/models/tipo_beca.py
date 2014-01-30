# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class tipoBeca(osv.Model):
	_name="becados.tipobeca"

	_order = 'tipo_beca'
	
	_rec_name = 'tipo_beca'
	
	_columns = {
		'tipo_beca': fields.char(string = "Tipo de Beca", size = 150, required = True),
	}


