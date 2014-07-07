# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	
	_inherit = 'ir.attachment'
	#~ _order = 'write_date desc'
	
	#Método para copiar el valor del campo de fecha de creación original al campo de fecha de creación local
	def _copiar_f_creacion(self, cr, uid, ids, context=None):
		values = {}
		
		browse_id = self.browse(cr, uid, ids, context=context)
		
		for reg in browse_id:
			ident = reg.id	#Pendiente por probar		
			f_c = reg.create_uid
		
		values.update({'fecha_creacion':f_c})
		
		return {'value':values}
		
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
		'nombre' : fields.binary("Nombre", required=False),
		'stage' : fields.char(string="Estado", required=False),
		'tipo_nomina' : fields.char(string="tipo_nomina", required=False),
		'tipo_beca' : fields.char(string="tipo_beca", required=False),
		'banco' : fields.char(string="Banco", required=False),
		'fecha_creacion' : fields.datetime(string="Fecha de creación", required=False)
		#~ 'categoria' : fields.char(string="Categoría", size=1, required=False),
		#~ El campo 'categoria' ha sido descartado como campo de identificación, en sustitución
		#~ se usará el campo 'res_model' que ya viene creado por defecto en este modelo 'ir.attachment'
	}
	
	_defaults = {
		'fecha_creacion' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
		#~ 'fecha_creacion' : _copiar_f_creacion,
	}
