# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from datetime import date

from openerp.osv import osv, fields

class Onchange_salary(osv.Model):
	_name="hr.change.salary"

	_order = 'salary'
	
	_rec_name = 'salary'

	
	def reason_change_salary(self, cr, uid, ids, context=None):

		salary_browse = self.browse(cr, uid, ids, context=None)
		data_ids = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		for many_load_salary in salary_browse:
			cedula          = many_load_salary.cedula
			experience 	= many_load_salary.experience
			salary_id 	= many_load_salary.salary
			charge_id 	= many_load_salary.charge.id
			degree_id 	= many_load_salary.degree_instruction.id

			print "Año de experiencia :"+str(cedula)

			if int(data_ids['experience'])==0: # Bloque de código para validar si el año de experencia no tiene valor

				cr.execute("UPDATE hr_employee SET asignacion=%s WHERE job_id=%s AND grado=%s;", (salary_id,charge_id,degree_id))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado	
			elif int(data_ids['experience'])!=0: #Bloque de código para validar si el año de experencia tiene valor

				cr.execute("UPDATE hr_employee SET asignacion=%s WHERE job_id=%s AND grado=%s AND ano_antiguedad=%s;", (salary_id,charge_id,degree_id,experience))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
			elif int(data_ids['cedula']): #Bloque de código para validar si el año de experencia tiene valor
				print "SOY PROCESO DE CEDULA INDIVIDUAL"
				#cr.execute("UPDATE hr_employee SET asignacion=%s WHERE job_id=%s AND grado=%s AND ano_antiguedad=%s;", (salary_id,charge_id,degree_id,experience))
				#self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
			return True

	def search_hr_data(self, cr, uid, ids, argument_search,item, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.job')

		if item == "1":
		
			#======================== Busqueda por cargo ============================
			search_job_id = obj_dp.search(cr, uid, [('id','=',argument_search)])

			datos_job_id = obj_dp.read(cr,uid,search_job_id,context=context)
			#========================================================================
			
			if datos_job_id:
				


				values.update({
					
					'salary' : datos_job_id[0]['asignacion'],
					'degree_instruction' : datos_job_id[0]['grado'],

					})

		elif item == '3':

			now = datetime.now().strftime('%Y-%m-%d')
			if argument_search < now or argument_search > now:
				
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe, no puede seleccionar una fecha distinta al actual, intente de nuevo...",
				}

				values.update({
					'date_now' : None,
					})

		return {'value' : values,'warning' : mensaje}
	
	
	_columns = {
		'salary': fields.char(string = "Sueldo", size = 7, required = True),
		'charge': fields.many2one("hr.job", "Cargo", required = False),
		'degree_instruction': fields.many2one("hr.config.asignacion", "Grado de Instruccción", required = False),
		'date_now': fields.date(string = "Fecha", required = True),
		'change_salary': fields.text(string = "Motivo del cambio", size = 256, required = False),
		'experience' : fields.char(string="Año de experiencia", size=2, required=False),
		'item' : fields.boolean(string="Año de experiencia"),
		'estado': fields.char(string = "Estado", size = 5, required = False),
		'usuario': fields.char(string = "Responsable", size = 20, required = False),
	}

	_defaults = {
		'usuario': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}



