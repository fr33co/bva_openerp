# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Departamento(osv.Model):
	_name = "becados.departamentos"
	
	_columns = {
		'departamento' : fields.char(string="Departamento", size=50, required=True),
	}
