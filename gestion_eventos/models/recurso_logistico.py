# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Grado(osv.Model):
	_name="gestion.recurso.logistico"

	_order = 'actividad'
	
	_rec_name = 'actividad'
	
	_columns = {
            # Recursos Logisticos
            'actividad' : fields.many2one('gestion.eventos','Actividad',required=False),
            'institucion': fields.many2one('gestion.inst.gerencia','Institución / Gerencia',required=False),
            'responsable': fields.char(string="Responsable", size=100, required=False),
            'recursos': fields.text(string="Recursos", size=500, required=False),
	}

	_defaults = {
		#'codigo' : 
	}



