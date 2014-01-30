# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Evaluacion(osv.Model):
	_name = "evaluacion.becados"
	_order = 'evaluado'
	_rec_name = 'evaluado'

	# Promedio de personal

	def promedio_personal(self, cr, uid, ids, puntaje_higiene,puntaje_uniforme,puntaje_rpersonales,puntaje_cortesia,puntaje_comunicacion,sub_total_1,sub_total_2,sub_total_3,sub_total_4, context=None):
	
	
		values = {}

		valores_sum = 0
		
		total_general = 0

		valores_sum = int(puntaje_higiene) + int(puntaje_uniforme) + int(puntaje_rpersonales) + int(puntaje_cortesia) + int(puntaje_comunicacion)
		
		total_general = self.puntuacion_total(sub_total_1,sub_total_2,sub_total_3,sub_total_4)
		
		values.update({

			'sub_total_1' : str(valores_sum)+" ptos",
			'total' : str(total_general)+" ptos",

			})
		return {'value' : values}

		

	# Promedio de sala

	def porcentaje_sala(self, cr, uid, ids, puntaje_atencion,puntaje_resolucion,puntaje_uso,sub_total_1,sub_total_2,sub_total_3,sub_total_4, context=None):

		values = {}

		valores_sum = 0
		
		total_general = 0

		#~ print puntaje_comunicacion+"PUNTOS"

		valores_sum = int(puntaje_atencion) + int(puntaje_resolucion) + int(puntaje_uso)
		
		total_general = self.puntuacion_total(sub_total_1,sub_total_2,sub_total_3,sub_total_4)
		
		values.update({

			'sub_total_2' : str(valores_sum)+" ptos",
			'total' : str(total_general)+" ptos",

			})
		return {'value' : values}
	

	# Promedio de organizacion

	def porcentaje_organizacion(self, cr, uid, ids, puntaje_atencion,sub_total_1,sub_total_2,sub_total_3,sub_total_4, context=None):

		values = {}

		valores_sum = 0
		
		total_general = 0

		#print puntaje_comunicacion+"PUNTOS"

		valores_sum = int(puntaje_atencion)
		
		total_general = self.puntuacion_total(sub_total_1,sub_total_2,sub_total_3,sub_total_4)

		values.update({

			'sub_total_3' : str(valores_sum)+" ptos",
			'total' : str(total_general)+" ptos",

			})
		return {'value' : values}

		

	# Promedio de desempeño de actividades

	def porcentaje_desempeno_actividades(self, cr, uid, ids, puntaje_manejo,puntaje_iniciativa,puntaje_pertenencia,sub_total_1,sub_total_2,sub_total_3,sub_total_4, context=None):

		values = {}

		valores_sum = 0
		
		total_general = 0

		#print puntaje_comunicacion+"PUNTOS"

		valores_sum = int(puntaje_manejo) + int(puntaje_iniciativa) + int(puntaje_pertenencia)
		
		total_general = self.puntuacion_total(sub_total_1,sub_total_2,sub_total_3,sub_total_4)

		values.update({

			'sub_total_4' : str(valores_sum)+" ptos",
			'total' : str(total_general)+" ptos",

			})
		return {'value' : values}
	
	# Cargar datos del becado
	
	def datos_becado(self, cr, uid, ids, cedula_becado, context=None):
		
		valores = {}
		
		alerta = {}
		
		if not cedula_becado:
			return valores
		
		#Preparación de los modelos donde se realizarán las búsquedas
		modelo1 = self.pool.get('evaluacion.becados')
		modelo2 = self.pool.get('hr.employee')
		
		#Ejecución de las búsquedas
		busqueda1 = modelo1.search(cr, uid, [('ci','=',cedula_becado)])
		busqueda2 = modelo2.search(cr, uid, [('cedula','=',cedula_becado)])
		
		
		if busqueda1:
			#Alerta
			#print "Está evaluado"
			alerta = {
				'title' : "Advertencia",
				'message' : "El becado ya ha sido evaluado, introdúzca otra cédula",
			}
			valores.update({
				'ci' : "",
				'evaluado' : "",
				'area' : "",
				'sede' : "",
			})
			return {'value' : valores, 'warning' : alerta}
		elif busqueda2:
			#Leer resultados y armar diccionario
			busqueda_leer = modelo2.read(cr, uid, busqueda2, context=context)
			
			valores.update({
				'evaluado' : busqueda_leer[0]['name_related'],
				'area' : busqueda_leer[0]['area'],
				'sede' : busqueda_leer[0]['sede'],
			})	
			return {'value' : valores}
		
		return 0
		
		
		'''def datos_becado(self, cr, uid, ids, cedula_becado, context=None):
		
		valores = {}
		
		alerta = {}
		
		if not cedula_becado:
			return valores
		
		#Preparación de los modelos donde se realizarán las búsquedas
		modelo1 = self.pool.get('evaluacion.becados')
		modelo2 = self.pool.get('hr.employee')
		
		#Ejecución de las búsquedas
		busqueda1 = modelo1.search(cr, uid, [('ci','=',cedula_becado)])
		busqueda2 = modelo2.search(cr, uid, [('cedula','=',cedula_becado)])
		
		
		if busqueda1:
			busqueda_leer1 = modelo1.read(cr, uid, busqueda1, context=context)
			#fecha = "Fecha de evaluación:"+str(busqueda_leer1[0]['fecha_actual'])
			#print fecha
			if(busqueda_leer1[0]['state'] == "confirmed" and self.limite_mes(busqueda_leer1[0]['fecha_actual']) == 0):
				#print busqueda_leer1[0]['state']
				alerta = {
					'title' : "Advertencia",
					'message' : "El becado ya ha sido evaluado, introdúzca otra cédula",
				}
				valores.update({
					'ci' : "",
					'evaluado' : "",
					'area' : "",
					'sede' : "",
				})
				return {'value' : valores, 'warning' : alerta}
			elif(busqueda_leer1[0]['state'] == "draft"):
				#print busqueda_leer1[0]['state']
				valores.update({
					'evaluado' : busqueda_leer1[0]['evaluado'],
					'area' : busqueda_leer1[0]['area'],
					'sede' : busqueda_leer1[0]['sede'],
				})
				return {'value' : valores}
		elif busqueda2:
			#Leer resultados y armar diccionario
			busqueda_leer2 = modelo2.read(cr, uid, busqueda2, context=context)
			
			valores.update({
				'evaluado' : busqueda_leer2[0]['name_related'],
				'area' : busqueda_leer2[0]['area'],
				'sede' : busqueda_leer2[0]['sede'],
			})	
			return {'value' : valores}
		
		return 0'''
		
	def limite_mes(self, fecha_evaluacion):
		#fecha_actual = date.today()
		fecha_act = "2014-02-21"
		fecha_actual = fecha_act.split("-")
		
		evaluacion = 0
		
		fecha_eval = fecha_evaluacion.split("-")
		
		#mes_actual = fecha_actual.month
		anyo_actual = fecha_actual[0]

		#dia_actual = fecha_actual.day
		mes_actual = fecha_actual[1]
		
		if int(fecha_eval[0]) <= int(anyo_actual):
			if int(fecha_eval[1]) < int(mes_actual):
				evaluacion = 1
				
		return evaluacion
		
	# Listar las cédulas de los becados registrados
	
	#~ def lista_becados(self, cr, user_id, context=None):
		#~ cr.execute('SELECT cedula FROM hr_employee')
		
		#~ lista = ()
		
		#~ for datos in cr.fetchall():
			#~ lista = lista + ((datos[0],datos[0]),)
		
		#~ return lista	
	
		
	# Puntaje total del becado
	
	def puntuacion_total(self,sub_total_1,sub_total_2,sub_total_3,sub_total_4):
		
		total_general = 0
		
		if not sub_total_1:
			total_general1 = 0
		else:
			total_general1 = int(sub_total_1[:-5]) # Equivalente a usar [:2], [0:2] o [0:-5] 

		if not sub_total_2:
			total_general2 = 0
		else:
			total_general2 = int(sub_total_2[:-5])
			
		if not sub_total_3:
			total_general3 = 0
		else:
			total_general3 = int(sub_total_3[:-5])
		
		if not sub_total_4:
			total_general4 = 0
		else:
			total_general4 = int(sub_total_4[:-5])

		total_general = total_general1 + total_general2 + total_general3 + total_general4

		return total_general


	def action_draft(self, cr, uid, ids, context=None):
	    #set to "draft" state
	    return self.write(cr, uid, ids, {'state':'draft'}, context=context)
	def action_confirm(self, cr, uid, ids, context=None):
	    #set to "confirmed" state
	    return self.write(cr, uid, ids, {'state':'confirmed'}, context=context)

	
	

	


	
	_columns = {
		# Datos Basicos
		'evaluado' : fields.char(string="Evaluado", size=50, required=True),
		'ci' : fields.char(string="Cédula", size=8, required=True),
		'area' : fields.many2one("becados.areas", string="Area de desempeño", required=True),
		'sede' : fields.many2one("becados.sedes", string="Sede", required=True),
		'fecha_actual' : fields.char(string="Fecha", size=256, readonly=True),
		'evaluador' : fields.char(string="Evaluador", size=256, required=True),
		# Pestañas NOTEBOOK Evaluacion

		'puntaje_higiene' : fields.selection((('4','4'),('3','3 '),('2','2'),('1','1'),('0','0')), "Higiene personal", required = True),
		'puntaje_uniforme' : fields.selection((('4','4'),('3','3 '),('2','2'),('1','1'),('0','0')), "Uso del uniforme", required = True),
		'puntaje_rpersonales' : fields.selection((('4','4'),('3','3 '),('2','2'),('1','1'),('0','0')), "Relaciones personales", required = True),
		'puntaje_cortesia' : fields.selection((('4','4'),('3','3 '),('2','2'),('1','1'),('0','0')), "Normas de cortesia", required = True),
		'puntaje_comunicacion' : fields.selection((('4','4'),('3','3 '),('2','2'),('1','1'),('0','0')), "Comunicación verbal y no verbal", required = True),
		'sub_total_1' : fields.char(string="sub-total", size=10, readonly=False),

		'puntaje_atencion' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Atención al cliente", required = True),
		'puntaje_resolucion' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Resolución de problemas", required = True),
		'puntaje_uso' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Uso de equipos personales e institucionales", required = True),
		'sub_total_2' : fields.char(string="sub-total", size=10, readonly=False),

		'puntaje_normas' : fields.selection((('20','20'),('19','19'),('18','18'),('17','17'),('16','16'),('15','15'),('14','14'),('13','13'),('12','12'),('11','11'),('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Normas y procedimientos", required = True),
		'sub_total_3' : fields.char(string="sub-total", size=10, readonly=False),

		'puntaje_manejo' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Manejo de las herramientas tecnológicas", required = True),
		'puntaje_iniciativa' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Iniciativa y creatividad", required = True),
		'puntaje_pertenencia' : fields.selection((('10','10'),('9','9'),('8','8'),('7','7'),('6','6'),('5','5'),('4','4'),('3','3'),('2','2'),('1','1'),('0','0')), "Sentido de pertenencia con la institución", required = True),
		'sub_total_4' : fields.char(string="sub-total", size=10, readonly=False),
		'calificacion_cuantitativa' : fields.selection((('Bueno','Bueno'),('Malo','Malo'),('Regular','Regular')), "Calificación", required = True),
		'observacion_general' : fields.text(string="Observación", size=256, required=True),
		'total' : fields.char(string="Puntuación total", readonly=False),
		'state' : fields.selection([('draft','Borrador'),
                            ('confirmed','Evaluado')], string="Estado"),

	}		

	#_sql_constraints = [
    #('ci_unique','UNIQUE(ci)','Disculpe esta cedula ya tiene asignada una novedad'),
	#]


	_defaults = {
		'fecha_actual': lambda *a: time.strftime("%d de %B del %Y"),# formato corecto al español

		'state': 'draft',

	} 

