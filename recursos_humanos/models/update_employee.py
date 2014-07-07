# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha
import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class Concepts_payslip(osv.Model):
	_name="hr.update.employee"

	_order = 'cedula'
	
	_rec_name = 'cedula'

	# M?TODO PARA EL REINGRESO DE PERSONAL

	def process_reingreso(self, cr, uid, ids, context=None):
		browse_slip_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)

		for x in browse_slip_id:

			cedula    = x.cedula
			nomina    = x.payslip.id
			employee  = x.emp_egre.id
			cargo     = x.charge_new.id
			depart    = x.dep_new.id
			sueldo    = x.sueldo_new
			reingreso = x.reingreso
			status    = "1"
			cr.execute("UPDATE hr_employee SET nomina=%s, class_personal=%s, job_id=%s, department_id=%s, asignacion=%s, fecha_ingreso=%s, status=%s  WHERE cedula=%s;", (nomina, employee, cargo, depart, sueldo, reingreso, status, cedula))
			cr.execute("UPDATE hr_movement_employee SET emp=%s, charge_acterior=%s, dep_lab=%s, sueldo=%s, date_ingreso=%s, status=%s, state=%s  WHERE cedula=%s;", (employee, cargo, depart, sueldo, reingreso, status, status, cedula))
			self.time_service_employee(cr,uid,ids,reingreso,cedula,context) # Metodo para actualizar el ano de servicio del empleado			
			self.write(cr, uid, ids, {'estado': '1'}, context=context) # Cambio de estado
		return True
	# Metodo para la busqueda de los datos del empleado
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
					'title'   : "Cambio de Nómina",
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

			}
			values.update(query)

		elif int(datos_code[0]['status']) !=7:
			mensaje = {
					'title'   : "Advertencia",
					'message' : "Disculpe el empleado no esta egresado...",
			}
			query = {
				'cedula': None,
			}
			values.update(query)
		else:

			query = {

				'date_ingreso' : datos_code[0]['fecha_ingreso'],
				'date_egreso' : datos_code[0]['fecha_egreso'],
				'charge_acterior' : datos_code[0]['job_id'],
				'nombres' : datos_code[0]['name_related'],
				'status' : datos_code[0]['status'],
				'emp' : datos_code[0]['class_personal'],
				'sueldo' : datos_code[0]['asignacion'],
				'dep_lab' : datos_code[0]['department_id'],

			}

			values.update(query)
		return {'value' : values,'warning' : mensaje}

	# Metodo para la carga de la signacion dependiendo el cargo que disponga
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

	def time_service_employee(self, cr, uid, ids, fecha_ingreso,cedula, context): 

		fecha = fecha_ingreso.split("-")

		ano = fecha[0]
		mes = fecha[1]
		dia = fecha[2]

		fecha_actual = date.today() # Fecha actual d/m/Y
		ano_actual = fecha_actual.year # Se optiene el año actual
		mes_actual = fecha_actual.month # Se optiene el mes actual
		dia_actual = fecha_actual.day # Se optiene el dia actual

		dia_diferencia = int(dia_actual) - int(dia)
		mes_diferencia = int(mes_actual) - int(mes)
		ano_diferencia = int(ano_actual) - int(ano)

		# se suma dia_diferencia los dias que tiene el mes acterior de la fecha actual

		if dia_diferencia < 0:
			mes_diferencia = int(mes_diferencia)-1

			if mes_actual:

				if mes_actual == 1 or mes_actual == 3 or mes_actual == 5 or mes_actual == 7 or mes_actual == 8 or mes_actual == 10 or mes_actual == 12:
					dias_mes_anterior = 31

				elif mes_actual == 2: # calculo si un año es bisiesto

					if ((((ano_actual%100)!=0) and ((ano_actual%4)==0)) or ((ano_actual%400)==0)):
						#print 'El año es Bisiesto'
						dias_mes_anterior = 29
					else:
						#print 'El año no es Bisiesto'
						dias_mes_anterior = 28

				elif mes_actual == 4 or mes_actual == 6 or mes_actual == 9 or mes_actual == 11:
					dias_mes_anterior = 30
			

			dia_diferencia = int(dia_diferencia) + int(dias_mes_anterior)

		if mes_diferencia < 0:
			ano_diferencia = int(ano_diferencia) - 1  
			mes_diferencia = int(mes_diferencia) + 12

		# Se valida si cumple un año se muestre año si es mayor de un año se muestre años
		if ano_diferencia < 2:
			ano_diferencia = str(ano_diferencia)+" Año"
		elif ano_diferencia > 1:
			ano_diferencia = str(ano_diferencia)+" Años"

		if mes_diferencia < 2:
			mes_diferencia = str(mes_diferencia)+" Mes"
		elif mes_diferencia > 1:
			mes_diferencia = str(mes_diferencia)+" Meses"

		if dia_diferencia < 2:
			dia_diferencia = str(dia_diferencia)+" Dia"
		elif dia_diferencia > 1:
			dia_diferencia = str(dia_diferencia)+" Dias"

		time_service   = str(ano_diferencia).replace('-',"")+" "+str(mes_diferencia)+" "+str(dia_diferencia) # dia, mes y ano de antiguedad
		ano_antiguedad = str(ano_diferencia).replace('-',"") # Ano de antiguedad
		cr.execute("UPDATE hr_employee SET ano_antiguedad=%s, tiempo_servicio=%s WHERE cedula=%s;", (ano_antiguedad, time_service, cedula)) # ano de antiguedad y tiempo de servicio para el objeto hr_employee
		cr.execute("UPDATE hr_movement_employee SET ano_servicio=%s WHERE cedula=%s;", (time_service, cedula)) # Tiempo de servicio para el modelo hr_movement_employee
		return time_service
	
	_columns = {
            'cedula': fields.char(string = "Cedula", size = 10, required = True),
            'nombres': fields.char(string = "Nombres / Apellidos", size = 150, required = False),
            'date_ingreso': fields.date(string = "Fecha de ingreso", required = False),
            'date_egreso': fields.date(string = "Fecha de egreso", required = False),
            #'ano_servicio': fields.char(string = "Años de servicio", size = 10, required = False),
            'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
            'charge_acterior': fields.many2one("hr.job", "Cargo", required = False),
            'sueldo': fields.char(string = "Sueldo Bs", size = 10, required = False),
            'dep_lab' : fields.many2one("hr.department", "Departamento", required = False),
		'emp' : fields.many2one("becados.clasper", "Empleado", required = False),
            'emp_egre' : fields.many2one("becados.clasper", "Empleado", required = True),
            'reingreso': fields.date(string = "Fecha de reingreso", required = True),
            'payslip' : fields.many2one("hr.nomina.adm", "Tipo nómina", required = True),
            'charge_new': fields.many2one("hr.job", "Cargo desempeñado", required = True),
            'dep_new' : fields.many2one("hr.department", "Departamento", required = True),
            'sueldo_new': fields.char(string = "Sueldo", size = 10, required = True),
            'observacion': fields.text(string = "Observación", size = 256, required = True),
	    'estado': fields.char(string = "Estado", size = 5, required = False),
	    'usuario': fields.char(string = "Responsable", size = 20, required = False),
	}

	_defaults = {
		'reingreso' : lambda *a: time.strftime("%Y-%m-%d"),
		'usuario': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}



