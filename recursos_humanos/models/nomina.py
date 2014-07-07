# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Banco(osv.Model):
	_name = "hr.nomina.adm"
	
	_order = "nomina"
	
	_rec_name = "nomina"
	
	_columns = {
		'cod' : fields.char(string="Código", size=10, required=False),
		'nomina' : fields.char(string="Nomina", size=50, required=False),
	}

