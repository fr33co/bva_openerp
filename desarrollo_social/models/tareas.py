# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class BecadoTarea(osv.Model):
	_name = "becado.tarea"
	
	_columns = {
		# Seccion III (Funciones del Cargo)
		'fecha' : fields.char(string="Fecha", readonly=True),
		'estudio' : fields.boolean(string="Estudia Actualmente?"),
		'especifique' : fields.char(string="Especifique", required=False),
		'funciones' : fields.text(string="Funciones Inherentes al Cargo", required=True),
		'observaciones' : fields.text(string="Observaciones", help="Llenado por el(la) Gerente de Desarrollo Social", required=False),
	}
	
	_defaults = {
		'fecha': lambda *a: time.strftime('%d-%m-%Y'),
	}
