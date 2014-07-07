# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Eje(osv.Model):
	_name="becados.ejes"

	_order = 'codigo'
	
	_rec_name = 'eje'
	
	_columns = {
		'codigo' : fields.char(string="Código", size=10, required=False),
		'eje': fields.char(string = "Eje", size = 150, required = True),
	}
