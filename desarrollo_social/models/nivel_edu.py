# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class NivelEduc(osv.Model):
	_name="becados.niveleduc"

	_order = 'nivel_edu'
	
	_rec_name = 'nivel_edu'
	
	_columns = {
		'grado_instruc' : fields.many2one("becados.gradoinstruccion","Grado de Instrucción",required=True),
		'nivel_edu': fields.char(string = "Nivel Educativo", size = 150, required = True),
	}
