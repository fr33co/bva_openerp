# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Novedades(osv.Model):
	_name = "novedades.becados"
	_order = 'encargado'
	_rec_name = 'encargado'
	
	def on_change_datos_personales(self, cr, uid, ids, becado, context=None):
		#print becado
		values = {}
		mensaje = {}
		
		if not becado:
			return values
		obj_dp = self.pool.get('hr.employee')

		busqueda = obj_dp.search(cr, uid, [('cedula','=',becado)])

		datos = obj_dp.read(cr,uid,busqueda,context=context)
		
		if not datos:
			#print "No existe intente de nuevo"
			
			mensaje = {
					'title'   : "Novedades del Becado",
					'message' : "Disculpe esta cedula no existe en la ficha de becado, intente de nuevo ",
			}
			
			
			values.update({
				
				'ci' : None,
				'nombres' : None,
				'direccion' : None,
				'tlf_movil' : None,
				'correo' : None,
				'sede' : None,

				})
			return {'value' : values,'warning' : mensaje}
			

		else:
			
			values.update({
				
				'sede' : datos[0]['sede'],
				'nombres' : datos[0]['name_related'],
				'direccion' : datos[0]['direccion'],
				'tlf_movil' : datos[0]['tlf_movil'],
				'correo' : datos[0]['correo'],

				})
			return {'value' : values}
			
		return 0

	
	_columns = {
		'encargado' : fields.char(string="Encargado de Eje:", size=256, required=True),
		'eje' : fields.selection((('Metro','Eje metro'),('Sur','Eje sur'),('Este','Eje este'),('Centro','Eje centro'),('Costa','Eje costa')), "Eje", required = True),
		#~ 'sede' : fields.char(string="Sede", size=256, required=True),
		'sede' : fields.many2one('becados.sedes','Sede',required=True),
		'fecha_actual' : fields.char(string="Fecha de Actual", required=True, readonly=True),
		'nombres' : fields.char(string="Nombre completo", size=256, required=True),
		
		'ci' : fields.char(string="Cédula", size=256, required=True),
		'novedad' : fields.char(string="Novedad", size=256, required=True),
		'observacion' : fields.char(string="Observación", size=256, required=True),
		'observacion_general' : fields.text(string="Observación General", size=256, required=True),
		'direccion' : fields.char(string="Dirección", size=256, required=True),
		'tlf_movil' : fields.char(string="Teléfono movil", size=256, required=True),
		'correo' : fields.char(string="Correo", size=256, required=True),
		'duration' : fields.char(string="Duración", size=256, required=False),
		
	}

	_sql_constraints = [
    ('ci_unique','UNIQUE(ci)','Disculpe esta cedula ya tiene asignada una novedad'),
	]


	_defaults = {
		'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español

	} 

