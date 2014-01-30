# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Concepto(osv.Model):
	_name = "becados.conceptos"
	
	_columns = {
		'concepto' : fields.char(string="Concepto", size=50, required=True),
		'formula' : fields.char(string="Fórmula", size=20, required=False),
		'monto' : fields.char(string="Monto", size=20, required=True),
	}

