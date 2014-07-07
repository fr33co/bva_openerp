# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

from openerp.osv import osv, fields

class Onchange_status(osv.Model):
	_name="hr.onchange.status"

	_order = 'cedula_employee'
	
	_rec_name = 'cedula_employee'

	# MÉTODO DE BUSQUEDA PARA CAMBIO DE ESTÁTUS

	def search_onchange_status(self, cr, uid, ids, argument_search,item, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.employee')

		if item == '1':

			#======================== Busqueda por código ============================

			search_obj_code = obj_dp.search(cr, uid, [('cedula','=',argument_search)])

			datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
			
			if not datos_code:
				
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe el registro no existe, intente de nuevo...",
				}

				values.update({
					
					'cedula_employee' : None,
					'nom' : None,
					'charge' : None,
					'status' : None,

					})
			elif str(datos_code[0]['status']) == "7": # En caso de que este en estado Egresado no permita la accion, debe proceder a reingrearlo
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe el empleado esta egresado para modificarlo debe proceder a reingresarlo...",
				}
				values.update({'cedula_employee' : None,})

			else:

				values.update({
					
					'nom' : datos_code[0]['name'],
					'charge' : datos_code[0]['job_id'],
					'status' : datos_code[0]['status'],

					})
		elif item == '3':

			now = datetime.now().strftime('%Y-%m-%d')
			if argument_search < now:
				
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe, no puede seleccionar una fecha anterior al actual, intente de nuevo...",
				}

				values.update({
					'date_onchange' : None,
					})
	
		return {'value' : values,'warning' : mensaje}

	
	def reason_change_read(self, cr, uid, ids, context=None):

		status_model = self.pool.get('hr.employee')

		status_browse = self.browse(cr, uid, ids, context=None)
		##########################################################################################
		obj_dp = self.pool.get('hr.movement.employee') # Objeto de llamado a hr.movement.employee
		obj_dpj = self.pool.get('hr.movement.payslip') # Objeto de llamado a hr.movement.payslip
		#########################################################################################
		
		for many_load_id in status_browse:

			id_fill = many_load_id.status
			cedula = many_load_id.cedula_employee
			date_now = many_load_id.date_onchange
			############################################################################################################################
			#						    ESTATUS ACTIVO
			############################################################################################################################
			if int(id_fill) == 1:
				search_obj_code = obj_dp.search(cr, uid, [('cedula','=',cedula),('nomina_admin','=',1)]) # Metodo para realizar la busqueda
				datos_code = obj_dp.read(cr,uid,search_obj_code,context=context) # Lectura del objeto a consultar
				
				for emp in datos_code: # Iteramos por la data del registro de asignaciones de nomina
					#id_concept = emp['movement_ids']
					nomina_id  = emp['nomina_admin'][1]
					
					search_obj = obj_dpj.search(cr, uid, [('cod','=',"208"),('tipo_nomina','=',nomina_id)]) # Metodo para realizar la busqueda
					datos = obj_dpj.read(cr,uid,search_obj,context=context) # Lectura del objeto a consultar
					
					for concept in datos:
						id_concept = concept['id']
						print "ID DEL CONCEPTO: "+str(concept['id'])
						print "CONCEPTO: "+str(concept['cod'])

				cr.execute("UPDATE hr_employee SET status=%s, fecha_egreso=%s WHERE cedula=%s;", (id_fill, date_now, cedula))
				cr.execute("UPDATE hr_movement_employee SET state=%s, status=%s WHERE cedula=%s;", (id_fill, id_fill, cedula))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				item = "1"
				cr.execute("UPDATE  hr_movement_payslip SET item='"+str(item)+"' WHERE cedula='"+str(cedula)+"' AND id='"+str(id_concept)+"';")
			############################################################################################################################
			#						    ESTATUS REPOSO
			############################################################################################################################
			elif int(id_fill) == 3:
				search_obj_code = obj_dp.search(cr, uid, [('cedula','=',cedula),('nomina_admin','=',1)]) # Metodo para realizar la busqueda
				datos_code = obj_dp.read(cr,uid,search_obj_code,context=context) # Lectura del objeto a consultar
				
				for emp in datos_code: # Iteramos por la data del registro de asignaciones de nomina
					#id_concept = emp['movement_ids']
					nomina_id  = emp['nomina_admin'][1]
					
					search_obj = obj_dpj.search(cr, uid, [('cod','=',"208"),('tipo_nomina','=',nomina_id)]) # Metodo para realizar la busqueda
					datos = obj_dpj.read(cr,uid,search_obj,context=context) # Lectura del objeto a consultar
					
					for concept in datos:
						id_concept = concept['id']
						print "ID DEL CONCEPTO: "+str(concept['id'])
						print "CONCEPTO: "+str(concept['cod'])

				cr.execute("UPDATE hr_employee SET status=%s, fecha_egreso=%s WHERE cedula=%s;", (id_fill, date_now, cedula))
				cr.execute("UPDATE hr_movement_employee SET state=%s, status=%s WHERE cedula=%s;", (id_fill, id_fill, cedula))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				item = "0"
				cr.execute("UPDATE  hr_movement_payslip SET item='"+str(item)+"' WHERE cedula='"+str(cedula)+"' AND id='"+str(id_concept)+"';")
			############################################################################################################################
			#						    ESTATUS SUSPENDIDO
			############################################################################################################################
			elif int(id_fill) == 5:
				cr.execute("UPDATE hr_employee SET status=%s, fecha_egreso=%s WHERE cedula=%s;", (id_fill, date_now, cedula))
				cr.execute("UPDATE hr_movement_employee SET state=%s, status=%s WHERE cedula=%s;", (id_fill, id_fill, cedula))
				cr.execute("UPDATE hr_ticket SET status=%s WHERE cedula=%s;", (id_fill, cedula))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
			############################################################################################################################
			#						    ESTATUS VACACIONES
			############################################################################################################################
			elif int(id_fill) == 6:
				
				search_obj_code = obj_dp.search(cr, uid, [('cedula','=',cedula),('nomina_admin','=',1)]) # Metodo para realizar la busqueda
				datos_code = obj_dp.read(cr,uid,search_obj_code,context=context) # Lectura del objeto a consultar
				
				for emp in datos_code: # Iteramos por la data del registro de asignaciones de nomina
					#id_concept = emp['movement_ids']
					nomina_id  = emp['nomina_admin'][1]
					
					search_obj = obj_dpj.search(cr, uid, [('cod','=',"208"),('tipo_nomina','=',nomina_id)]) # Metodo para realizar la busqueda
					datos = obj_dpj.read(cr,uid,search_obj,context=context) # Lectura del objeto a consultar
					
					for concept in datos:
						id_concept = concept['id']
						print "ID DEL CONCEPTO: "+str(concept['id'])
						print "CONCEPTO: "+str(concept['cod'])

				cr.execute("UPDATE hr_employee SET status=%s, fecha_egreso=%s WHERE cedula=%s;", (id_fill, date_now, cedula))
				cr.execute("UPDATE hr_movement_employee SET state=%s, status=%s WHERE cedula=%s;", (id_fill, id_fill, cedula))
				self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				item = "0"
				cr.execute("UPDATE  hr_movement_payslip SET item='"+str(item)+"' WHERE cedula='"+str(cedula)+"' AND id='"+str(id_concept)+"';")
			############################################################################################################################
			#						    ESTATUS EGRESADO
			############################################################################################################################
			elif int(id_fill) == 7:

				######################################################################################
				search_obj_code = obj_dp.search(cr, uid, [('cedula','=',cedula),('nomina_admin','=',1)]) # Metodo para realizar la busqueda
				datos_code = obj_dp.read(cr,uid,search_obj_code,context=context) # Lectura del objeto a consultar
				monto = 0.00
				asignacion = 0.00
				deduccion  = 0.00
				for emp in datos_code: # Iteramos por la data del registro de asignaciones de nomina
					ced = emp['cedula']
					
					search_obj = obj_dpj.search(cr, uid, [('cedula','=',ced)]) # Metodo para realizar la busqueda
					datos = obj_dpj.read(cr,uid,search_obj,context=context) # Lectura del objeto a consultar
					
					for concept in datos:
						id_concept = concept['id']
						cedula = concept['cedula']
					
						monto      = "0.00"
						asignacion = "0.00"
						deduccion  = "0.00"
						cr.execute("DELETE FROM hr_movement_payslip WHERE id='"+str(id_concept)+"' AND cedula='"+str(cedula)+"';") # Accion para depurar los conceptos del empleado cuando este en estado Egresado

					cr.execute("UPDATE hr_employee SET status=%s, fecha_egreso=%s WHERE cedula=%s;", (id_fill, date_now, cedula))
					cr.execute("UPDATE hr_movement_employee SET state=%s, status=%s, monto_c=%s, monto_asignacion=%s, monto_deduccion=%s WHERE cedula=%s;", (id_fill, id_fill, monto, asignacion,deduccion, cedula))
					cr.execute("UPDATE hr_ticket SET status=%s WHERE cedula=%s;", (id_fill, cedula))
					self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				######################################################################################

		return True
	
	
	_columns = {
		'cedula_employee': fields.char(string = "Cédula", size = 10, required = True),
		'nom': fields.char(string = "Nombres", size = 256, required = False),
		'charge': fields.many2one("hr.job", "Cargo", required = False),
		#'status': fields.many2one("becados.status", "Estátus", required = True),
		'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
		'date_onchange': fields.date(string = "Fecha", required = True),
		'reason_change': fields.text(string = "Descripción", size = 256, required = True),
		'estado': fields.char(string = "Estado", size = 5, required = False),
		'usuario': fields.char(string = "Responsable", size = 20, required = False),
	}

	_defaults = {
		'date_onchange' : lambda *a: time.strftime("%Y-%m-%d"),
		'usuario': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}



