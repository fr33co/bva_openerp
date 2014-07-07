# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class InstitucionEduc(osv.Model):
	_name="becados.institucioneduc"

	_order = 'institucion_edu'
	
	_rec_name = 'institucion_edu'
	
	_columns = {
		'nombre_corto' : fields.char(string="Nombre Corto",requierd=False),
		'institucion_edu': fields.char(string = "Institución", size = 150, required = True),
	}

