# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class TCuenta(osv.Model):
	_name = "becados.tipocuenta"
	
	_columns = {
		't_cuenta' : fields.char(string="Tipo de Cuenta", size=30, required=True),
	}
