# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class tipo_acciones_centralizadas(osv.Model):

	_name = "tipo.accion.centralizada"
	
	_rec_name ="a_centralizada"	
	_columns = {
		
		'a_centralizada' : fields.char(string="Acción Centralizada", required=False),
		
	}
	
class tipo_acciones_especificas(osv.Model):

	_name = "tipo.accion.especifica"

	_rec_name ="a_especifica"
	_columns = {
		
		'a_especifica' : fields.char(string="Acción Específica", required=False),
		'a_centralizada': fields.many2one('tipo.accion.centralizada', 'Acción Centralizada', required=True),
	}