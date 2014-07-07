# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Carga_familiar(osv.Model):
	_name = "becado.carga.familiar"

	def validar_fecha(self, cr, uid, ids, fecha_nac_familiar):

		values = {}

		edad = fecha_nac_familiar

		edades = edad.split("-")

		fecha_actual = date.today()# Obtenemos el Ano actual der servidor

		ano_actual = fecha_actual.year # Segmentamos la fecha y obtenemos el ano actual

		mes_actual = fecha_actual.month

		dia_actual = mes_actual = fecha_actual.day


		calculo = int(ano_actual) - int(edades[0])
			
		if int(edades[1] > int(mes_actual)):
			calculo = calculo - 1
		elif (int(edades[1]) == int(mes_actual)) and (int(edades[2]) > int(dia_actual)):
			calculo = calculo - 1 

		values.update({

			'edad' : calculo,

			})
		return {'value' : values}

	def on_change_datos_personales(self, cr, uid, ids, becado, context=None):
		values = {}
		if not becado:
			return values
		obj_dp = self.pool.get('hr.employee')


		busqueda = obj_dp.search(cr, uid, [('id','=',becado)])

		busqueda_read = obj_dp.read(cr,uid,busqueda,context=context)

		values.update({
			#~ 'primer_nombre' : busqueda_read[0]['primer_nombre'],
			#~ 'segundo_nombre' : busqueda_read[0]['segundo_nombre'],
			#~ 'primer_apellido' : busqueda_read[0]['primer_apellido'],
			#~ 'segundo_apellido' : busqueda_read[0]['segundo_apellido'],
			'nombre_completo' : busqueda_read[0]['name_related'],

			})
		return {'value' : values}

	
	_columns ={
		#Sección I (Datos del Becado)
		'becado' : fields.many2one('hr.employee','Becado',required=False, domain=[('category_ids.name','=','Becados')]),
		'cedula_becado' : fields.char(string = "Cédula", size = 9, required = False, help="Cédula del Becado"),
		'nombre_completo' : fields.char(string = "Nombre Completo", required = False, help="Nombre Completo del Becado"),
		'primer_nombre' : fields.char(string="Primer nombre", help="Ingrese el primer nombre", required = False),
		'segundo_nombre' : fields.char(string="Segundo nombre", help="Ingrese el segundo nombre", required = False),
		'primer_apellido' : fields.char(string="Primer apellido", help="Ingrese el primer apellido", required = False),
		'segundo_apellido' : fields.char(string="Segundo apellido", help="Ingrese el segundo apellido", required = False),
		'edad' : fields.char(string="Edad", help="Ingrese la Edad", required = False),
		
		#Sección II (Datos del Familiar)
		'cedula_familiar': fields.char(string = "Cédula Familiar", size = 9, required = False, help="Cédula del familiar"),
		'primer_nombres_familiar' : fields.char(string="Primer nombre", help="Ingrese el primer nombre del Familiar", required = True),
		'segundo_nombre_familiar' : fields.char(string="Segundo nombre", help="Ingrese el segundo nombre del Familiar", required = False),
		'primer_apellido_familiar' : fields.char(string="Primer apellido", help="Ingrese el primer apellido del Familiar", required = True),
		'segundo_apellido_familiar' : fields.char(string="Segundo apellido", help="Ingrese el segundo apellido del Familiar", required = False),
		'fecha_nac_familiar': fields.date(string = "Fecha de Nacimiento", required = True),
		'profesion_familiar' : fields.char(string="Profesión u Oficio", help="Ingrese la Profesión u Oficio del Familiar", required = False),
		'sexo' : fields.selection((('1','Masculino'),('2','Femenino')), "Sexo", required = True),
		'parentesco' : fields.selection((('1','Hijo(a)'),('2','Madre'),('3','Padre'),('4','Esposo(a)'),('5','Unión Estable')), "Parentesco", required = True),
		'estudio' : fields.boolean(string="Estudia Actualmente?"),
		'fecha_union' : fields.date(string="Fecha de la Unión", required=False),
		'telefono_fijo' : fields.char(string="Teléfono Fijo", size=12, required=False),
		'telefono_movil' : fields.char(string="Teléfono Móvil", size=12, required=False),
		'correo' : fields.char(string="Correo electrónico", size=50, required=False),
		'direccion' : fields.text(string="Dirección", size=256, required=True),
		
	}

	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]

