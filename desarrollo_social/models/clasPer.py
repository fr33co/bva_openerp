# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class clasPer(osv.Model):
	_name="becados.clasper"

	_columns = {
		'clas_personal': fields.char(string = "Clasificación del Personal", size = 150, required = True),
	}

