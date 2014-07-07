# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Institucion_gerencia(osv.Model):
	_name="gestion.inst.gerencia"

	_order = 'name'
	
	_rec_name = 'name'
	
	_columns = {

		'name': fields.char(string = "Nombre", size = 256, required = True),
		'gerente' : fields.char(string = "Responsable", size = 100, required = False),
		'compania': fields.many2one('res.company','Compañia',required=False),
	}

	_defaults = {
		#'codigo' : 
	}



