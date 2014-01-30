# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Potencialidad(osv.Model):
	_name = "consejocomunal.potencialidades"
	
	_columns = {
		'potencialidad' : fields.char(string="Potencialidad", size=100, required=True),
	}
	
	_order = 'potencialidad'
	_rec_name = 'potencialidad'
