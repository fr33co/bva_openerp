# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class tipoBeca(osv.Model):
	_name="becados.tipobeca"

	_order = 'tipo_beca'
	
	_rec_name = 'tipo_beca'
	
	_columns = {
		'cod_beca' : fields.char(string="Código beca",required=False),
		'cod_t_beca' : fields.char(string="Código tipo beca",required=False),
		'tipo_beca' : fields.char(string = "Tipo de Beca", size = 150, required = True),
		'asignacion' : fields.float(string="Asignación",required=True),
		'descripcion' : fields.text(string = "Descripción", required=False, help = "Indique las funciones inherentes al tipo de beca"),
	}
