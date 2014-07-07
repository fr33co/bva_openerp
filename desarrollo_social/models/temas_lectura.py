# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Temas_lectura(osv.Model):
	_name = "consejocomunal.temas_lectura"
	
	_columns = {
		'nombre_tema' : fields.char(string="Nombre del Tema", size=50, required=True),
	}
	
	_order = 'nombre_tema'
	_rec_name = 'nombre_tema'
