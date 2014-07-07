# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha
import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields
from openerp.tools.translate import _
class Shuttle_ascent_employee(osv.Model):
	_name="hr.shuttle.ascent.employee"

	_order = 'cedula'

	_rec_name = 'cedula'

	# METODO PARA EL REINGRESO DE PERSONAL (FILTRO)

	def process_data_emp(self, cr, uid, ids, context=None):
		browse_slip_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)

		for x in browse_slip_id:
			#=======================================
			cargo_anterior    = x.charge_acterior.id
			cargo_nuevo       = x.charge_new.id
			#=======================================
			depart_anterior    = x.dep_lab.id
			depart_nuevo       = x.dep_new.id
			cedula             = x.cedula
			sueldo             = x.sueldo_new
			#=======================================
			
			if str(x.movimiento) == '1':

				if int(depart_nuevo) == int(depart_anterior):
					raise osv.except_osv(_("Warning!"), _("La nueva dependencia debe ser distinta al que posee actualmente..."))
				else:
					cr.execute("UPDATE hr_employee SET department_id=%s, asignacion=%s  WHERE cedula=%s;", (depart_nuevo, sueldo, cedula))
					self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				return True

			elif str(x.movimiento) == '2':

				if int(cargo_nuevo) == int(cargo_anterior):
					raise osv.except_osv(_("Warning!"), _("El nuevo cargo debe ser distinto al que posee actualmente..."))
				else:
					cr.execute("UPDATE hr_employee SET job_id=%s, asignacion=%s  WHERE cedula=%s;", (cargo_nuevo, sueldo, cedula))
					self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				return True

			elif str(x.movimiento) == '3':
				if int(cargo_nuevo) == int(cargo_anterior):
					raise osv.except_osv(_("Warning!"), _("El nuevo cargo debe ser distinto al que posee actualmente..."))
			
				elif int(depart_nuevo) == int(depart_anterior):
					raise osv.except_osv(_("Warning!"), _("La nueva dependencia debe ser distinta al que posee actualmente..."))

				else:
					cr.execute("UPDATE hr_employee SET job_id=%s, department_id=%s, asignacion=%s  WHERE cedula=%s;", (cargo_nuevo, depart_nuevo, sueldo, cedula))
					self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
				return True


	def data_employee(self, cr, uid, ids, argument_search, context=None):

		values = {}
		mensaje = {}

		if not argument_search:

			return values
		obj_dp = self.pool.get('hr.employee')

		#======================== Busqueda por c?digo ============================

		search_obj_code = obj_dp.search(cr, uid, [('cedula','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)

		#=========================================================================
		#print datos_code
		if not datos_code:

			mensaje = {
					'title'   : "Cambio de N?mina",
					'message' : "Disculpe el registro no existe, intente de nuevo...",
			}
			query = {

				'date_ingreso' : None,
				'date_egreso' : None,
				'charge_acterior' : None,
				'nombres' : None,
				'status' : None,
				'emp' : None,
				'sueldo' : None,
				'dep_lab' : None,
				'cedula': None,

			}
			values.update(query)

		elif int(datos_code[0]['status']) == 7:
			mensaje = {
					'title'   : "Advertencia",
					'message' : "Disculpe el empleado esta egresado para modificarlo debe reingresarlo...",
			}
			query = {
				'cedula': None,
			}
			values.update(query)
		elif int(datos_code[0]['status']) == 5:
			mensaje = {
					'title'   : "Advertencia",
					'message' : "Disculpe el empleado no se encuentra activo actualmente...",
			}
			query = {
				'cedula': None,
			}
			values.update(query)
		else:

			query = {

				'date_ingreso' : datos_code[0]['fecha_ingreso'],
				'ano_servicio' : datos_code[0]['tiempo_servicio'],
				'charge_acterior' : datos_code[0]['job_id'],
				'nombres' : datos_code[0]['name_related'],
				'status' : datos_code[0]['status'],
				'emp' : datos_code[0]['class_personal'],
				'sueldo' : datos_code[0]['asignacion'],
				'dep_lab' : datos_code[0]['department_id'],
				'image' : datos_code[0]['image_medium'],
				'charge_new' : datos_code[0]['job_id'],
				'dep_new' : datos_code[0]['department_id'],

			}

			values.update(query)
		return {'value' : values,'warning' : mensaje}


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

					'sueldo_new' : datos_job_id[0]['asignacion'],

					})

		return {'value' : values,'warning' : mensaje}



	_columns = {
            'cedula': fields.char(string = "Cedula", size = 10, required = True),
            'nombres': fields.char(string = "Nombres / Apellidos", size = 150, required = False),
            'date_ingreso': fields.date(string = "Fecha de ingreso", required = False),
            'ano_servicio': fields.char(string = "Servicio", size = 10, required = False),
            'status' : fields.selection((('1','Activo'),('2','Peri?do de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
            'charge_acterior': fields.many2one("hr.job", "Cargo", required = False),
            'sueldo': fields.char(string = "Sueldo Bs", size = 10, required = False),
            'dep_lab' : fields.many2one("hr.department", "Departamento", required = False),
	    'emp' : fields.many2one("becados.clasper", "Empleado", required = False),
            'reingreso': fields.date(string = "Fecha de reingreso", required = True),
            'movimiento' : fields.selection((('1','Traslado'),('2','Ascenso'),('3','Traslado / Ascenso')), "Movimiento", required = True),
            'charge_new': fields.many2one("hr.job", "Cargo desempe?ado", required = True),
            'dep_new' : fields.many2one("hr.department", "Departamento", required = True),
            'sueldo_new': fields.char(string = "Sueldo", size = 10, required = True),
            'observacion': fields.text(string = "Observaci?n", size = 256, required = True),
            'image' : fields.binary("",help="Empleado"),
	    'estado': fields.char(string = "Estado", size = 5, required = False),
	    'usuario': fields.char(string = "Responsable", size = 20, required = False),
	}

	_defaults = {
		'reingreso' : lambda *a: time.strftime("%Y-%m-%d"),
		'usuario': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}



