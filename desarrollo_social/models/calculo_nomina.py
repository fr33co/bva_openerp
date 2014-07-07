# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class CalcNom(osv.Model):
	_inherit = 'hr.payslip.line'

	_columns = {
		'asignacion': fields.float(string = "Asignación", required = False),
	}
