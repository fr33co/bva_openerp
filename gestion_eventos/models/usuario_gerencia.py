# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class User_gerencia(osv.Model):
	_name="gestion.usuario"

	_order = 'gerencia'
	
	_rec_name = 'gerencia'
	
	_columns = {

		'usuario': fields.many2one("res.users", "Usuario", required = False),
		'gerencia': fields.many2one('gestion.inst.gerencia','Institución / Gerencia',required=False),
	}

	_defaults = {
		#'codigo' : 
	}



