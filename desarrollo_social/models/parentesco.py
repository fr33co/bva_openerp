# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Parentesco(osv.Model):
	_name = "becados.parentescos"
	
	_columns = {
		'parentesco' : fields.char(string="Parentesco", size=30, required=True),
	}

