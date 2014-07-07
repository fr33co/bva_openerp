# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class Curriculum(osv.Model):
	_name = 'becados.seleccion'

	_columns = {
		'postulante': fields.many2one("","Postulante", required = False),
	}

