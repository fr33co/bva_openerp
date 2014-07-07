# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Empleado(osv.Model):
	
	'''Herenciando a hr_applicant (empleados)'''
	
	#_order = "empleado"
	
	_inherit = 'hr.applicant'

	def case_close_emp(self, cr, uid, ids, context=None):

		
		# Método browse para hr.applicant (capturar datos del aspirante a empleado)
		data_browse = self.browse(cr, uid, ids, context=None)

		for hr_applicant in data_browse:
			name_c			= hr_applicant.partner_name
			cedula 			= hr_applicant.cedula
			email  			= hr_applicant.email_from
			phone  			= hr_applicant.partner_phone
			mobile 			= hr_applicant.partner_mobile
			grade  			= hr_applicant.grado_instruccion.id
			direction 		= hr_applicant.direccion_trabajo
			experience		= hr_applicant.ano_experiencia
			charge			= hr_applicant.job_id.id
			department 		= hr_applicant.department_id.id
			country			= hr_applicant.country.id
			state			= hr_applicant.estado.id
			municipality	= hr_applicant.municipality.id
			parish			= hr_applicant.parish.id

			# print "Cargo:"+str(charge)
			# print "Departamento:"+str(department)

			# Método Write para rescribir el estatus a Contratado
			self.write(cr, uid, ids, {'status':'2'}, context=context)

			# Diccionario de datos

			data_applicant = {
							'name':name_c,
							'cedula':cedula,
							'correo':email,
							'tlf_local':phone,
							'tlf_movil':mobile,
							'grado_instruccion':grade,
							'direccion':direction,
							'ano_antiguedad':experience,
							'job_id':charge,
							'department_id':department,
							'country_id':country,
							'estado':state,
							'ciudad':'16',
							'municipio':municipality,
							'parroquia':parish,
							'categoria':'2',
							'status_employee':'1',}
			
			# Metodo para la inserción de los datos del candidato a la ficha de Empleado
			self.pool.get('hr.employee').create(cr,uid,data_applicant, context=context)

		return True

	
	_columns = {
		'date_now' : fields.char(string="fecha", size = 50, required=False),
		'grado_instruccion': fields.many2one("becados.gradoinstruccion", "Grado de Instrucción", required = True),
		'country' : fields.many2one("res.country", "Pais", required = True),
		'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		'municipality' : fields.many2one("res.country.municipality", "Municipio", required = True, select="0"),
		'parish' : fields.many2one("res.country.parish", "Parroquia", required = True, select="0"),
		'admin' : fields.boolean(string="Administración"),
		'cap' : fields.boolean(string="Capacidad analítica"),
		'com' : fields.boolean(string="Comunicación escrita"),
		'trab' : fields.boolean(string="Trabajo bajo presión"),
		'c_oral' : fields.boolean(string="Comunicación oral"),
		'lid' : fields.boolean(string="Liderazgo"),
		'neg' : fields.boolean(string="Negociación"),
		'otros_a' : fields.boolean(string="Otros"),
		'act' : fields.boolean(string="Actitud al cambio"),
		'inic' : fields.boolean(string="Iniciativa/Creatividad"),
		'mot' : fields.boolean(string="Motivación"),
		'resp' : fields.boolean(string="Responsabilidad"),
		'trab_e' : fields.boolean(string="Trabajo en equipo"),
		'otros_b' : fields.boolean(string="Otros"),
		'status' : fields.selection((('1','Activo'),('2','Contratado')), "Estatus", required = False),

	}
	
	_defaults = {
		'date_now': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español
		'country': 240,
		'status' : '1',
		
	} 
