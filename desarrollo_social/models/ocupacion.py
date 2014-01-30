# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Ocupacion(osv.Model):
	_name = "consejocomunal.ocupaciones"
	
	_columns = {
		'ocupacion' : fields.char(string="Ocupación", size=100, required=True),
	}
	
	_order = 'ocupacion'
	_rec_name = 'ocupacion'
