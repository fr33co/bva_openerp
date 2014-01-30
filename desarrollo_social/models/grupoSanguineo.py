# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class grupoSanguineo(osv.Model):
	_name="becados.gruposanguineo"
	
	_order = 'grupo_sang'
	
	_rec_name = 'grupo_sang'

	_columns = {
		'grupo_sang': fields.char(string = "Grupo Sanguíneo", size = 150, required = True),
	}


