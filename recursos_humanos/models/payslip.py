# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Nomina_payslip(osv.Model):
	_name="proceso.payslip"

	_order = 'id_slip'
	
	_rec_name = 'id_slip'
	
	_columns = {
		'id_slip': fields.integer(string = "Nómina"),
		'id_employee': fields.integer(string = "Empleado"),
	}

	_defaults = {
		#'codigo' : 
	}



