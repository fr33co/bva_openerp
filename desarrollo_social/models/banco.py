# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Banco(osv.Model):
	_name = "becados.bancos"
	
	_columns = {
		'nombre_corto' : fields.char(string="Nombre Corto", size=10, required=False),
		'banco' : fields.char(string="Entidad Bancaria", size=50, required=True),
	}

