# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha
import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final

class Onchange_slip(osv.Model):
	_name="hr.change.slip"

	_order = 'cedula_employee'
	
	_rec_name = 'cedula_employee'

	# MÉTODO DE BUSQUEDA PARA CAMBIO DE NÓMINA


	def search_onchange_slip(self, cr, uid, ids, argument_search, context=None):

		values  = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.employee')
		
		#======================== Busqueda por cédula ============================

		search_obj_code = obj_dp.search(cr, uid, [('cedula','=',argument_search)])

		datos_code      = obj_dp.read(cr,uid,search_obj_code,context=context)
		
		#=========================================================================
		if int(datos_code[0]['status']) == 5:
			mensaje = {
					'title'   : "Cambio de Nómina",
					'message' : "Disculpe el personal se encuentra suspendido...",
			}
			values.update({'cedula_employee' : None,})
			
		elif int(datos_code[0]['status']) == 7:
			mensaje = {
					'title'   : "Cambio de Nómina",
					'message' : "Disculpe el personal se encuentra egresado...",
			}
			values.update({'cedula_employee' : None,})
		elif not datos_code:
			
			mensaje = {
					'title'   : "Cambio de Nómina",
					'message' : "Disculpe el registro no existe, intente de nuevo...",
			}
			
			values.update({
				
				'cedula_employee' : None,
				'nom' : None,
				'charge' : None,
				'slip' : None,
				'type_employee' : None,
				'slip_change' : None,

				})

		else:

			values.update({
				
				'nom' :           datos_code[0]['name'],
				'charge' :        datos_code[0]['job_id'],
				'slip' :          datos_code[0]['nomina'],
				'type_employee' : datos_code[0]['class_personal'],

				})

			
		return {'value' : values,'warning' : mensaje}

	
	def reason_change_slip(self, cr, uid, ids, context=None):

		status_model  = self.pool.get('hr.employee')
		slip_browse = self.browse(cr, uid, ids, context=None)
		
		for many_load_slip in slip_browse:

			id_slip          = many_load_slip.slip.id
			id_type_employee = many_load_slip.type_employee.id
			filter_employee  = many_load_slip.cedula_employee
			# print "CEDULA: "+str(filter_employee)
			# print "ID DE NOMINA: "+str(id_slip)
			# print "ID TIPO EMPLEADO: "+str(id_type_employee)

			cr.execute("UPDATE hr_employee SET nomina=%s, class_personal=%s WHERE cedula=%s;", (id_slip, id_type_employee, filter_employee))
			
		return True

	def change_slip_date(self, cr, uid, ids, fecha, context=None):
		values = {}
		validar_fecha = {}
		now = datetime.now().strftime('%Y-%m-%d')
		if fecha < now:
			
			validar_fecha = {
					'title'   : "Cambio de estátus",
					'message' : "Disculpe, no puede seleccionar una fecha anterior al actual, intente de nuevo...",
			}

			values.update({
				'date_onchange' : None,
				})

		return {'value' : values,'warning' : validar_fecha}

	
	
	_columns = {
		'cedula_employee': fields.char(string = "Cédula", size = 9, required = True),
		'nom': fields.char(string = "Nombres", size = 256, required = False),
		'charge': fields.many2one("hr.job", "Cargo", required = False),
		# #'status': fields.many2one("becados.status", "Estátus", required = True),
		'slip' : fields.many2one("hr.nomina.adm", "Nómina", required = False),
		'type_employee' : fields.many2one("becados.clasper", "Tipo empleado", required = False),
		'date_onchange': fields.date(string = "Fecha", required = True),
		'slip_change': fields.text(string = "Descripción", size = 256, required = True),
	}

	_defaults = {
		'date_onchange' : lambda *a: time.strftime("%Y-%m-%d"),
	}



