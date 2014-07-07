# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class plan_gobierno(osv.Model):

	_name = "plan.gobierno"
	
	_rec_name ="plan_gobierno"	
	_columns = {
		
		'plan_gobierno' : fields.char(string="Plan de Gobierno", required=True),
		
	}
	
class lineas_estrategicas_accion(osv.Model):

	_name = "lineas.estrategicas"

	_rec_name ="lineas_estrategicas"
	_columns = {
		
		'lineas_estrategicas' : fields.char(string="Líneas estratégicas de accion", required=False),
		'plan_gobierno': fields.many2one('plan.gobierno', 'Plan de Gobierno', required=True),
	}

class linea_estrategica_objetivos_escpeficos(osv.Model):

	_name = "lineas.objetivos.escpeficos"

	_columns = {
		
		'obj_especificos' : fields.text(string="Objetivos Específicos", required=False),
		'plan_gobierno': fields.many2one('plan.gobierno', 'Plan de Gobierno', required=True),
		'lineas_estrategicas': fields.many2one('lineas.estrategicas', 'Lineas estrategicas de Accion', required=True),
	}