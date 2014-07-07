# -*- coding: utf-8 -*-

#21.05.2014 23:49:34

import time # Necesario para las funciones de Fecha
import os
from datetime import date
from openerp.osv import osv, fields
from openerp.tools.translate import _

# CLASE DE MOVIMIENTOS ASIGNADOS A LA NOMINA
class Movement_employee_payslip(osv.Model):
	_name="hr.movement.employee"
	
	_order = 'cedula' # Ordenamos por cedula del empleado
	_order = 'nomina_admin' # Ordenamos por nominas
	_rec_name = 'nombres'
	##################################################################################################################
	#
	##################################################################################################################
	
	def actualizar(self, cr, uid, ids, context=None): # Metodo para Recalcular los montos cuando surja un cambio de la asignacion del empleado
		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		data_ids = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		
		for emp_id in browse_data:
			cedula = emp_id.cedula
		
		hr_emp = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
	
		search_emp  = hr_emp.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
		hr_employee = hr_emp.read(cr,uid,search_emp,context=context) # Se refleja el resultado
		
		for emp in hr_employee:
			sm = float(emp['asignacion']) # ASIGNACION DEL EMPLEADO
			fecha_in = emp['fecha_ingreso']
			print "SIGNACION: "+str(sm)
		
		for x in browse_data:
			filtro_id = x.id
			asig      = x.sueldo
			ids_id    = data_ids['movement_ids']

		get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
		
		search_get_hr = get_hr.search(cr, uid, [('id','=',ids_id),('asig_deduc','=',filtro_id)], context=None) # Se busca el ID dado
		employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
		porcentaje = ""
		for e in employee_cod:
			cod = e['cod']
			cantidad_d = e['cantidad_d']
			cantidad_h = e['cantidad_h']
			if str(cantidad_d) == "False": cantidad_d = ""
			elif str(cantidad_h) == "False": cantidad_h = ""
			else:
				if str(e['cod']) == "456": # Procesar calcular de nuevo el concepto 456
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_1 = (sm/dias*0.12)*can
					print "CALCULO CONCEPTO 456: "+str(operador_1)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_1))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				if str(e['cod']) == "101": # Procesar calcular de nuevo el concepto 101
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_2 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 101: "+str(operador_2)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_2))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "102": # Procesar calcular de nuevo el concepto 101
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_102 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 102: "+str(operador_102)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_102))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "008": # Procesar calcular de nuevo el concepto 008
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_3 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 008: "+str(operador_3)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_3))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				if str(e['cod']) == "009": # Procesar calcular de nuevo el concepto 009
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_4 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 009: "+str(operador_4)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_4))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				if str(e['cod']) == "103": # Procesar calcular de nuevo el concepto 103
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_5 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 103: "+str(operador_5)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_5))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				if str(e['cod']) == "125": # Procesar calcular de nuevo el concepto 125
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_6 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 125: "+str(operador_6)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_6))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				if str(e['cod']) == "116": # Procecar calcular de nuevo el concepto 116
					fecha = fecha_in.split("-")

					ano = fecha[0]
					mes = fecha[1]

					fecha_actual = date.today() # Fecha actual d/m/Y
					ano_actual = fecha_actual.year # Se optiene el año actual
					mes_actual = fecha_actual.month # Se optiene el mes actual

					mes_diferencia = int(mes_actual) - int(mes)
					ano_diferencia = int(ano_actual) - int(ano)
					
					ano_dif = int(ano_diferencia)
					#print "ANO DIFERENCIA: "+str(ano_dif)
					diferencia = str(ano_dif).replace('-',"") # Se renplaza el valor negativo a positivo de la cifra
					
					if int(diferencia) == 0 or int(diferencia) == 1 or int(diferencia) == 2:
						raise osv.except_osv(_("Warning!"), _("Disculpe no puede ser cargado el concepto, debe disponer de mas de 3 años de servicio..."))
					elif int(diferencia) == 3:
						porcentaje = 0.04
					elif int(diferencia) == 4:
						porcentaje = 0.05
					elif int(diferencia) == 5:
						porcentaje = 0.06
					elif int(diferencia) == 6:
						porcentaje = 0.07
					elif int(diferencia) == 7:
						porcentaje = 0.08
					elif int(diferencia) == 8:
						porcentaje = 0.09
					elif int(diferencia) > 8:
						porcentaje = 0.1

					monto      = float(sm)
					can        = ""
					operador_7   = monto * porcentaje # Concepto 116 Prima de Antiguedad
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_7))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
					print "CALCULO CONCEPTO 116: "+str(operador_7)
				
				if str(e['cod']) == "134": # Procesar calcular de nuevo el concepto 134
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_8 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 134: "+str(operador_8)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_8))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "148": # Procesar calcular de nuevo el concepto 148
					dias = int(cantidad_d)
					# can  = int(cantidad_h)
					operador_9 = ((sm/dias)*float(1.5))
					print "CALCULO CONCEPTO 148: "+str(operador_9)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_9))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "183": # Procesar calcular de nuevo el concepto 183
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_10 = float(sm)/int(dias)*1*int(can)
					print "CALCULO CONCEPTO 183: "+str(operador_10)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_10))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "143": # Procesar calcular de nuevo el concepto 148
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_11 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 143: "+str(operador_11)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_11))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "149": # Procesar calcular de nuevo el concepto 149
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_12 = ((sm/dias/int(7))*0.3)*can
					result      = redondear(operador_12)
					print "CALCULO CONCEPTO 149: "+str(operador_12)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(result)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")	
				
				if str(e['cod']) == "150": # Procesar calcular de nuevo el concepto 150
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_13 = ((sm/dias/int(8))*1.5)*can
					print "CALCULO CONCEPTO 150: "+str(operador_13)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_13))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "151": # Procesar calcular de nuevo el concepto 151
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_15 = ((sm/dias/int(7))*1.95)*can
					print "CALCULO CONCEPTO 151: "+str(operador_15)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_15))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "184": # Procesar calcular de nuevo el concepto 184
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_14 = float(sm)/int(dias)*1*int(can)
					print "CALCULO CONCEPTO 184: "+str(operador_14)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_14))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "456": # Procesar calcular de nuevo el concepto 456
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_16 = (sm/dias*0.12)*can
					print "CALCULO CONCEPTO 456: "+str(operador_16)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_16))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")	

				if str(e['cod']) == "102": # Procesar calcular de nuevo el concepto 102
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_17 = ((sm/dias)*can)
					print "CALCULO CONCEPTO 102: "+str(operador_17)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_17))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "182": # Procesar calcular de nuevo el concepto 182
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_18 = (sm/dias*0.04)*can
					print "CALCULO CONCEPTO 182: "+str(operador_18)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_18))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "462": # Procesar calcular de nuevo el concepto 462
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_19 = (sm/dias*0.12)*can
					print "CALCULO CONCEPTO 462: "+str(operador_19)
					cr.execute("UPDATE hr_movement_payslip SET asignacion='"+str(redondear(operador_19))+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "502": # Procesar calcular de nuevo el concepto 502
					dias = int(cantidad_d)
					result = sm*int(12)/int(52)*0.04*int(dias)
					operador_20 = "%.2f" % round(result,2) # Concepto SSO
					print "CALCULO CONCEPTO 502: "+str(operador_20)
					cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(operador_20)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")

				if str(e['cod']) == "561": # Procesar calcular de nuevo el concepto 561
					dias = int(cantidad_d)
					result = sm*int(12)/int(52)*0.005*int(dias)
					operador_21 = "%.2f" % round(result,2) # Concepto SSO
					print "CALCULO CONCEPTO 561: "+str(operador_21)
					cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(operador_21)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")				
				
				if str(e['cod']) == "590":
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
					search_get_hr = get_hr.search(cr, uid, [('asig_deduc','=',filtro_id),('incidencia','=','si')], context=None) # Se busca el ID dado
					employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

					sum_incidencias = 0
					for i in employee_cod:
						sum_incidencias += float(i['asignacion']) # Sumatoria de los conceptos que tengan incidencias salariales
						result_incidencia = (float(sum_incidencias))*0.01 # Formula del concepto (590)s F.A.O.V Monto para fraccion de quincena
					monto = result_incidencia # Resultado de la operacion
					deduc       = float(monto)
					deduccion   = "%.2f" % round(deduc,2)
					cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "514": # Recalcular los conceptos 514 (Diferencia SSO y 562 (Diferencia LRPE))
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_concept = get_hr.search(cr, uid, [('cod','=','102'),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					concepts = get_hr.read(cr,uid,search_concept,context=context) # Se refleja el resultado

					if not concepts:
						raise osv.except_osv(_("Warning!"), _("Disculpe el concepto (102) Diferencia  de sueldo no existe, intente de nuevo..."))
					else:
						dias = int(cantidad_d)
						concepto_102 = float(concepts[0]['asignacion'])
						operador =concepto_102*int(12)/int(52)*0.04*int(dias)
						deduc       = float(operador)
						deduccion   = "%.2f" % round(deduc,2)
						cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "562": # Recalcular los conceptos 514 (Diferencia SSO y 562 (Diferencia LRPE))
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_concept = get_hr.search(cr, uid, [('cod','=','102'),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					concepts = get_hr.read(cr,uid,search_concept,context=context) # Se refleja el resultado

					if not concepts:
						raise osv.except_osv(_("Warning!"), _("Disculpe el concepto (102) Diferencia  de sueldo no existe, intente de nuevo..."))
					else:
						dias = int(cantidad_d)
						concepto_102 = float(concepts[0]['asignacion'])
						operador =concepto_102*int(12)/int(52)*0.005*int(dias)
						deduc       = float(operador)
						deduccion   = "%.2f" % round(deduc,2)
						cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "622": #Recalcular el concepto 622 Diferencia de caja de ahorro
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr.movement.payslip (Nomina)
					get_hr_ced = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
		
					# Bloque de codigo para el modelo hr.movement.payslip (Asignacion y Deduccion del personal)
					search_concept = get_hr.search(cr, uid, [('cod','=','102'),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					concepts = get_hr.read(cr,uid,search_concept,context=context) # Se refleja el resultado
					
					concept = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					concepts_2 = get_hr.read(cr,uid,concept,context=context) # Se refleja el resultado
					
					
					browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
					for x in browse_data:
						cedula = x.cedula
					# Bloque de codigo para el modelo hr.employee (Personal)
					search_get_hr = get_hr_ced.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
					employee = get_hr_ced.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				
					for i in employee:
						
						if not concepts:
							raise osv.except_osv(_("Warning!"), _("Disculpe el concepto (102) Diferencia  de sueldo no existe como asignacion, intente de nuevo..."))
						elif str(i['caja_ahorro']) == "False":
							raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no se retiene ningun porcentaje de caja de ahorro..."))
						else:
							if str(i['caja_ahorro']) == "10":
								caja_ahorro = 0.1
							else:
								caja_ahorro = 0.05
				
							concepto_102 = float(concepts[0]['asignacion'])
				
							operador = concepto_102*caja_ahorro # Formula para el calculo Diferencia caja de ahorro ya sea con el 5 o 10 porciento
							deduc       = float(operador)
							deduccion   = "%.2f" % round(deduc,2)
							cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
					
				if str(e['cod']) == "601":
					browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro

					for x in browse_data:
						cedula = x.cedula

					get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
					employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

					for i in employee:
						asignacion  = i['asignacion']
						if str(i['caja_ahorro']) == "False":
							raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no se retiene ningun porcentaje de caja d ahorro..."))
						elif str(i['caja_ahorro']) == "10":
							caja_ahorro = 0.1
						else:
							caja_ahorro = 0.05
					operador   = asignacion * caja_ahorro
					deduc       = float(operador)
					deduccion   = "%.2f" % round(deduc,2)
					cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
				
				if str(e['cod']) == "903": # recalculo del concepto 903 (Inasistencia Injustificada)
					dias = int(cantidad_d)
					can  = int(cantidad_h)
					operador_903 = ((sm/dias)*can)
					deduc       = float(operador_903)
					deduccion   = "%.2f" % round(deduc,2)
					print "CALCULO CONCEPTO 903: "+str(operador_903)
					cr.execute("UPDATE hr_movement_payslip SET deduccion='"+str(deduccion)+"' WHERE cod='"+str(cod)+"' AND asig_deduc='"+str(filtro_id)+"';")
					
		self.buscar(cr, uid, ids, context) # METODO DE BUSQUEDA
		self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones

	def borrar(self, cr, uid, ids, context=None): # METODO PARA BORRAR LOS DATOS DEL ONE2MANY (TREE) ASIGNACIONES Y DEDUCCIONES DE LA NOMINA

		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		data_ids = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		for x in browse_data:
			filtro_id = x.id
			cod       = x.codigo_delete # Codigo Regular
			cod_vac   = x.codigo_delete_vac # Codigo vacaciones

		if str(x.nomina_admin.tipo_nomina) == "Regular": # NOMINA REGULAR
			product_obj = self.pool.get('hr.movement.payslip')
			product_id  = product_obj.search(cr, uid, [('asig_deduc','=',filtro_id),('cod','=',cod)])
			read_x      = product_obj.read(cr,uid,product_id,context=context)

			if not data_ids['codigo_delete']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el codigo de concepto, intente de nuevo..."))
				return False

			elif not read_x:
				raise osv.except_osv(_("Warning!"), _("Disculpe el codigo de concepto no existe, intente de nuevo..."))
				return False
			else:
				product_obj.unlink(cr, uid, [read_x[0]['id']], context=None) # Borro el codigo perteneciente al concepto con el metodo unlink()
				self.write(cr, uid, ids, {'codigo_delete': None}, context=context) # Reseteo los valores a vacio
				self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':''}, context=context) # Reseteo los valores a vacio
				accion = self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones
				self.buscar(cr, uid, ids, context)
				self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones
			return accion
		elif str(x.nomina_admin.tipo_nomina) == "Vacaciones": # NOMINA VACACIONES
			product_obj = self.pool.get('hr.movement.payslip.vacaciones')
			product_id = product_obj.search(cr, uid, [('asig_deduc_vac','=',filtro_id),('cod','=',cod_vac)])
			read_x = product_obj.read(cr,uid,product_id,context=context)

			if not data_ids['codigo_delete_vac']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el codigo de concepto, intente de nuevo..."))
				return False
			elif not read_x:
				raise osv.except_osv(_("Warning!"), _("Disculpe el codigo de concepto no existe, intente de nuevo..."))
				return False
			else:
				product_obj.unlink(cr, uid, [read_x[0]['id']], context=None) # Borro el codigo perteneciente al concepto con el metodo unlink()
				self.write(cr, uid, ids, {'codigo_delete_vac': None}, context=context) # Reseteo los valores a vacio
				self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':''}, context=context) # Reseteo los valores a vacio
				accion = self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones
				self.buscar(cr, uid, ids, context)
				self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones
			return accion
	
	def resetear(self, cr, uid, ids, context=None): # METODO PARA RESETEAR LOS VALORES
		self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':''}, context=context) # Reseteo los valores a vacio
		self.buscar(cr, uid, ids, context)
		self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones
		
	def promediar_calculo(self, cr, uid, ids, context=None): # METODO PARA REALIZAR EL PROMEDIO DEL SALARIO INTEGRAL
		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		data_ids = self.read(cr, uid, ids, context=context)[0]
		movement_id = data_ids['movement_ids']
		movement_vac_id = data_ids['vacaciones_ids']

		obj_dp = self.pool.get('hr.movement.payslip') # Nomina Regular
		obj_vac = self.pool.get('hr.movement.payslip.vacaciones') # Nomina vacaciones
		#======================== Busqueda por codigo ============================
		for x in browse_data:
			nomina = x.nomina_admin.tipo_nomina

		if str(nomina) == "Regular": # NOMINA REGULAR

			search_obj_code1 = obj_dp.search(cr, uid, [('id','=',movement_id),('filtro','=','1')])
			calculos1 = obj_dp.read(cr,uid,search_obj_code1,context=context)
			asignacion = 0
			
			for x in calculos1:

				asignacion += float(x['asignacion'])

			search_obj_code2 = obj_dp.search(cr, uid, [('id','=',movement_id),('filtro','=','2')])
			calculos2 = obj_dp.read(cr,uid,search_obj_code2,context=context)
			deduccion  = 0
			for x in calculos2:
				deduccion += float(x['deduccion'])

			salario_integral = asignacion - deduccion

			self.write(cr, uid, ids, {'monto_asignacion': "%.2f" % round(asignacion,2)}, context=context) # Reseteo los valores a vacio
			self.write(cr, uid, ids, {'monto_deduccion': "%.2f" % round(deduccion,2)}, context=context) # Reseteo los valores a vacio
			self.write(cr, uid, ids, {'monto_c': "%.2f" % round(salario_integral,2)}, context=context) # Reseteo los valores a vacio
			#=========================================================================
		elif str(nomina) == "Vacaciones": # NOMINA REGULAR

			search_obj_code1 = obj_vac.search(cr, uid, [('id','=',movement_vac_id),('filtro','=','1')])
			calculos1 = obj_vac.read(cr,uid,search_obj_code1,context=context)
			asignacion = 0
			deduccion  = 0
			for x in calculos1:

				asignacion += float(x['asignacion'])

			search_obj_code2 = obj_vac.search(cr, uid, [('id','=',movement_vac_id),('filtro','=','2')])
			calculos2 = obj_vac.read(cr,uid,search_obj_code2,context=context)
			for x in calculos2:
				deduccion += float(x['deduccion'])

			salario_integral = asignacion - deduccion

			self.write(cr, uid, ids, {'monto_asignacion_vac': "%.2f" % round(asignacion,2)}, context=context) # Reseteo los valores a vacio
			self.write(cr, uid, ids, {'monto_deduccion_vac': "%.2f" % round(deduccion,2)}, context=context) # Reseteo los valores a vacio
			self.write(cr, uid, ids, {'monto_c_vac': "%.2f" % round(salario_integral,2)}, context=context) # Reseteo los valores a vacio
			#=========================================================================


	def buscar(self, cr, uid, ids, context=None): # METODO DE BUSQUEDA

		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
		for x in browse_data:
			cedula = x.cedula
		#======================== Busqueda por c?digo ============================
		obj_dp = self.pool.get('hr.employee')
		search_obj_code = obj_dp.search(cr, uid, [('cedula','=',cedula)])
		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)

		obj_slip = self.pool.get('hr.movement.employee')
		#=========================================================================

		if datos_code:

			obj_slip.write(cr, uid, [x.id], {'date_ingreso': datos_code[0]['fecha_ingreso'],
						  'ano_servicio': datos_code[0]['tiempo_servicio'],
						  'charge_acterior': datos_code[0]['job_id'][0],
						  'nombres': datos_code[0]['name_related'],
						  'status': datos_code[0]['status'],
						  'emp': datos_code[0]['class_personal'][0],
						  'sueldo': "%.2f" % round(datos_code[0]['asignacion'],2), # SE REDONDEA LA SIFRA A DOS DIGITOS
						  'dep_lab': datos_code[0]['department_id'][0],
						  'image': datos_code[0]['image_medium']}, context=context)
	
	def calculo_asig(self, cr, uid, ids, context=None):
		values = {}
		###################################################################################
		#		METODO PARA CALCULAR ASIGNACIONES / DEDUCCIONES OBRERO
		###################################################################################
		browse_data     = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)
		data_asig_deduc = self.read(cr, uid, ids, context=context)[0] # Validacion para campos vacio
		
		for emp_id in browse_data:
			sueldo_emp = emp_id.cedula
		
		hr_emp = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
	
		search_emp  = hr_emp.search(cr, uid, [('cedula','=',sueldo_emp)], context=None) # Se busca el ID dado
		hr_employee = hr_emp.read(cr,uid,search_emp,context=context) # Se refleja el resultado
		
		for emp in hr_employee:
			sueldo        = emp['asignacion'] # ASIGNACION DEL EMPLEADO
			fecha_ingreso = emp['fecha_ingreso'] 
		
		for x in browse_data:
			###############################################################################
			# Bloque de calculo (1) por formula (variantes)
			###############################################################################
			#if str(x.emp.clas_personal) != "Obrero":
			#	raise osv.except_osv(_("Warning!"), _("Disculpe no se aplica este concepto... escoja otro que corresponda al empleado Administrativo"))

			if not data_asig_deduc['sueldo']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe realizar la busqueda de los datos del empleado en el boton ((Buscar))..."))
			elif not data_asig_deduc['codigo']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el codigo de concepto..."))
			# elif str(x.nomina_admin.tipo_nomina) !="Regular":
			# 		raise osv.except_osv(_("Warning!"), _("Disculpe no corresponde a la nomina Regular, intente de nuevo..."))
			# Formulas aplicadas para el concepto (008,009,101,103,125,134,143)
			elif str(x.codigo) == "008" or str(x.codigo) == "009" or str(x.codigo) == "101" or str(x.codigo) == "103" or str(x.codigo) == "125" or str(x.codigo) == "134" or str(x.codigo) == "143" or str(x.codigo) == "150" or str(x.codigo) == "151" or str(x.codigo) == "456" or str(x.codigo) == "102" or str(x.codigo) == "182" or str(x.codigo) == "462":
				
				if not data_asig_deduc['sueldo']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe realizar la busqueda de los datos del empleado en el boton ((Buscar))..."))
				
				elif not data_asig_deduc['cant_horas']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
			
				elif not data_asig_deduc['cant_dias']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
				
				
				else:
				
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
	
					search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
					
					cod = ""
					for i in employee_cod:
						cod = i['cod']
						print "CODIGO: "+str(i['cod'])
						print "CONCEPTO: "+str(i['descripcion'])
					
					if cod == x.codigo: # Proceso de validacion si existe el concepto no permita registrarlo
						self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
					else:
						sm    = float(sueldo)
						dias  = int(x.cant_dias)
						can   = int(x.cant_horas)

						if str(x.codigo) == "150":
							operador = ((sm/dias/8)*1.5)*can # Formula 008,009,101,103,125,134,143,150
						elif str(x.codigo) == "151":
							operador = ((sm/dias/7)*1.95)*can
						elif str(x.codigo) == "456":
							operador = (sm/dias*0.12)*can
						elif str(x.codigo) == "102": # Concepto diferencia de sueldo
							operador = (sm/dias)*can
						elif str(x.codigo) == "182": # Diferencia prima de antiguedad
							operador = (sm/dias*0.04)*can
						elif str(x.codigo) == "462": # Diferencia prima por profesionalizacion
							operador = (sm/dias*0.12)*can
						else:
							operador = ((sm/dias)*can) # Formula 008,009,101,103,125,134,143,150
						frecuencia = ""
						deduccion = ""
						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"
						
						# Se registra el concepto 008,009
						
						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = str(x.cant_dias)+"/"+str(x.cant_horas)
						asig        = float(operador)
						asignacion  = "%.2f" % round(asig,2)
						deduccion   = deduccion
						asig_deduc  =  x.id
						filtro      = "1"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
			###################################################################################
			# Bloque de calculo (2) por monto unico
			###################################################################################
			
			
			elif str(x.codigo) == "104" or str(x.codigo) == "107" or str(x.codigo) == "208" or str(x.codigo) == "210" or str(x.codigo) == "249" or str(x.codigo) == "168" or str(x.codigo) == "154" or str(x.codigo) == "303" or str(x.codigo) == "304" or str(x.codigo) == "305" or str(x.codigo) == "306" or str(x.codigo) == "509" or str(x.codigo) == "605" or str(x.codigo) == "606" or str(x.codigo) == "607" or str(x.codigo) == "608" or str(x.codigo) == "519" or str(x.codigo) == "604" or str(x.codigo) == "908" or str(x.codigo) == "903" or str(x.codigo) == "185":
				
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				cod = ""
				for i in employee_cod:
					cod = i['cod']
				
				if cod == x.codigo:

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio

				elif str(x.codigo) == "903":
					if not data_asig_deduc['cant_horas']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el campo Cantidad/Horas..."))

					elif not data_asig_deduc['cant_dias']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el campo Cantidad/Dias..."))

					else:
						frecuencia = ""
						asignacion = ""
						deduccion = ""
						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"

						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = str(x.cant_dias)+"/"+str(x.cant_horas)
						asig_deduc  =  x.id

						sm    = float(x.sueldo)
						dias  = int(x.cant_dias)
						can   = int(x.cant_horas)
						operador = (sm/dias)*can
						deduc  = float(operador)
						asignacion  = ""
						deduccion   = "%.2f" % round(deduc,2)
						filtro      = "2"
						nomina      = x.nomina_admin.id
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
				else:

					if not data_asig_deduc['sueldo']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe realizar la busqueda de los datos del empleado en el boton <<Buscar>> antes de procesar cualquier accion..."))

					elif not data_asig_deduc['monto']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor a calcular..."))
					else:
						get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

						search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
						employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
						cod = ""
						for i in employee_cod:
							cod = i['cod']

						if cod == x.codigo:

							self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio

						else:
							monto      = x.monto
							operador   = monto # Formula 104,243,107,208,181,210,249,168,154,303,304,305,306
							frecuencia = ""
							deduccion  = ""
							if int(x.frecuencia) == 1:
								frecuencia = "F"
							elif int(x.frecuencia) == 2:
								frecuencia = "E"

							# Se registra el concepto 008,009

							cedula      = x.cedula
							cod         = x.codigo
							frecuencia  = frecuencia
							descripcion =  x.consulta.concepto
							cantidad    = ""
							asig_deduc  =  x.id

							if str(x.codigo) == "509" or str(x.codigo) == "605" or str(x.codigo) == "606" or str(x.codigo) == "607" or str(x.codigo) == "608" or str(x.codigo) == "519" or str(x.codigo) == "604" or str(x.codigo) == "908":

								deduc  = float(operador)

								asignacion  = ""
								deduccion   = "%.2f" % round(deduc,2)
								filtro      = "2"
								nomina      = x.nomina_admin.id
								self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

							else:
								if str(x.codigo) == "185":
									if int(x.monto) > 1700:
										raise osv.except_osv(_("Warning!"), _("Disculpe el monto que ingreso excede de 1700, intente de nuevo..."))
									asig  = float(operador)
									deduccion  = ""
									asignacion   = "%.2f" % round(asig,2)
									filtro      = "1"
									nomina      = x.nomina_admin.id
									self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
									
								else:

									if str(x.codigo) == "210":
										
										browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro

										for x in browse_data:
											cedula = x.cedula

										get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

										search_get_hr = get_hr.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
										employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

										for i in employee:
											if str(i['marital']) == "False" or str(i['marital']) == "": # Validacion al momento del estado civil del empleado para la asignacion de la prima de hogar
												raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no cumple con la prima de hogar..."))
											elif int(i['marital']) == 1:
												raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no cumple con la prima de hogar, esta Soltero..."))
											else:
												asig  = float(operador)
												deduccion  = ""
												asignacion   = "%.2f" % round(asig,2)
												filtro      = "1"
												nomina      = x.nomina_admin.id
												self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
									else:
										print "SOY LOS CONCEPTOS DEL 303 AL 306"
										asig  = float(operador)
										
										deduccion  = ""
										asignacion   = "%.2f" % round(asig,2)
										filtro      = "1"
										nomina      = x.nomina_admin.id
										self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			###################################################################################
			elif str(x.codigo) == "116" or str(x.codigo) == "102" or str(x.codigo) == "601": # Concepto 116 Prima por antiguedad

				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				cod = ""
				for i in employee_cod:
					cod = i['cod']
				
				if cod == x.codigo:

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio

				elif str(x.codigo) == "601":
					browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro

					for x in browse_data:
						cedula = x.cedula

					get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
					employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

					for i in employee:
						asignacion  = i['asignacion']
						if str(i['caja_ahorro']) == "False":
							raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no se retiene ningun porcentaje de caja d ahorro..."))
						elif str(i['caja_ahorro']) == "10":
							caja_ahorro = 0.1
						else:
							caja_ahorro = 0.05

					operador   = asignacion * caja_ahorro
					frecuencia = ""
					deduccion  = ""

					if int(x.frecuencia) == 1:
						frecuencia = "F"
					elif int(x.frecuencia) == 2:
						frecuencia = "E"

					# Se registra el concepto 008,009

					cedula      = x.cedula
					cod         = x.codigo
					frecuencia  = frecuencia
					descripcion =  x.consulta.concepto
					cantidad    = ""
					asignacion  = ""
					deduc       = float(operador)
					deduccion   = "%.2f" % round(deduc,2)
					asig_deduc  =  x.id
					filtro      = "2"
					nomina      = x.nomina_admin.id
					# Salida de los datos al modelo movimientos (hr.movement.payslip)
					self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

				else:

					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
					cod = ""
					
					for i in employee_cod:
						cod = i['cod']
					
					if cod == x.codigo:

						self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
					
					else:
						fecha = fecha_ingreso.split("-")
						
						ano = fecha[0]
						mes = fecha[1]

						fecha_actual = date.today() # Fecha actual d/m/Y
						ano_actual = fecha_actual.year # Se optiene el año actual
						mes_actual = fecha_actual.month # Se optiene el mes actual

						mes_diferencia = int(mes_actual) - int(mes)
						ano_diferencia = int(ano_actual) - int(ano)
						
						ano_dif = int(ano_diferencia)
						#print "ANO DIFERENCIA: "+str(ano_dif)
						diferencia = str(ano_dif).replace('-',"") # Se renplaza el valor negativo a positivo de la cifra
						
						if int(diferencia) == 0 or int(diferencia) == 1 or int(diferencia) == 2:
							raise osv.except_osv(_("Warning!"), _("Disculpe no puede ser cargado el concepto, debe disponer de mas de 3 años de servicio..."))
						elif int(diferencia) == 3:
							porcentaje = 0.04
						elif int(diferencia) == 4:
							porcentaje = 0.05
						elif int(diferencia) == 5:
							porcentaje = 0.06
						elif int(diferencia) == 6:
							porcentaje = 0.07
						elif int(diferencia) == 7:
							porcentaje = 0.08
						elif int(diferencia) == 8:
							porcentaje = 0.09
						elif int(diferencia) > 8:
							porcentaje = 0.1

						monto      = float(x.sueldo)
						can        = ""
						operador   = monto * porcentaje# Concepto 116 Prima de Antiguedad
						frecuencia = ""
						deduccion  = ""

						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"

						# Se registra el concepto 008,009

						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						asig        = float(operador)
						asignacion  = "%.2f" % round(asig,2)
						deduccion   = deduccion
						asig_deduc  =  x.id
						filtro      = "1"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			elif str(x.codigo) == "514" or str(x.codigo) == "562":
				
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				cod = ""
				for i in employee_cod:
					cod = i['cod']
				if not data_asig_deduc['monto']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la cantidad de lunes..."))
				
				elif cod == x.codigo:

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_concept = get_hr.search(cr, uid, [('cod','=','102'),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					concepts = get_hr.read(cr,uid,search_concept,context=context) # Se refleja el resultado

					if not concepts:
						raise osv.except_osv(_("Warning!"), _("Disculpe el concepto (102) Diferencia  de sueldo no existe, intente de nuevo..."))
					else:
						concepto_102 = float(concepts[0]['asignacion'])

						if str(x.codigo) == "514":

							operador =concepto_102*int(12)/int(52)*0.04*int(x.monto)
						else:
							operador =concepto_102*int(12)/int(52)*0.005*int(x.monto)

						frecuencia = ""
						asignacion = ""

						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"

						# Se registra el concepto 502

						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						asignacion  = asignacion
						deduc       = float(operador)
						deduccion   = "%.2f" % round(deduc,2)
						asig_deduc  =  x.id
						filtro      = "2"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			elif str(x.codigo) == "622":
				
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr.movement.payslip (Nomina)
				get_hr_ced = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)
	
				# Bloque de codigo para el modelo hr.movement.payslip (Asignacion y Deduccion del personal)
				search_concept = get_hr.search(cr, uid, [('cod','=','102'),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				concepts = get_hr.read(cr,uid,search_concept,context=context) # Se refleja el resultado
				
				concept = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				concepts_2 = get_hr.read(cr,uid,concept,context=context) # Se refleja el resultado
				
				cod = ""
				for i in concepts_2:
					cod = i['cod']
				if cod == x.codigo:

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:
					browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro
					for x in browse_data:
						cedula = x.cedula
					# Bloque de codigo para el modelo hr.employee (Personal)
					search_get_hr = get_hr_ced.search(cr, uid, [('cedula','=',cedula)], context=None) # Se busca el ID dado
					employee = get_hr_ced.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				
					for i in employee:
						
						if not concepts:
							raise osv.except_osv(_("Warning!"), _("Disculpe el concepto (102) Diferencia  de sueldo no existe como asignacion, intente de nuevo..."))
						elif str(i['caja_ahorro']) == "False":
							raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no se retiene ningun porcentaje de caja de ahorro..."))
						else:
							if str(i['caja_ahorro']) == "10":
								caja_ahorro = 0.1
							else:
								caja_ahorro = 0.05
				
							concepto_102 = float(concepts[0]['asignacion'])
				
							operador = concepto_102*caja_ahorro # Formula para el calculo Diferencia caja de ahorro ya sea con el 5 o 10 porciento
				
							frecuencia = ""
							asignacion = ""
				
							if int(x.frecuencia) == 1:
								frecuencia = "F"
							elif int(x.frecuencia) == 2:
								frecuencia = "E"
				
							# Se registra el concepto 622
				
							cedula      = x.cedula
							cod         = x.codigo
							frecuencia  = frecuencia
							descripcion =  x.consulta.concepto
							cantidad    = ""
							asignacion  = asignacion
							deduc       = float(operador)
							deduccion   = "%.2f" % round(deduc,2)
							asig_deduc  =  x.id
							filtro      = "2"
							nomina      = x.nomina_admin.id
							# Salida de los datos al modelo movimientos (hr.movement.payslip)
							self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			elif str(x.codigo) == "502" or str(x.codigo) == "561":

				if not data_asig_deduc['monto']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la cantidad de lunes..."))
				else:
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
					cod = ""
					for i in employee_cod:
						cod = i['cod']

					if cod == x.codigo:
						self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
					else:
						
						sm         = float(x.sueldo)
						if str(x.codigo) == "502":
							operador   = sm*int(12)/int(52)*0.04*int(x.monto) # Concepto SSO
						else:
							operador   = sm*int(12)/int(52)*0.005*int(x.monto) # Concepto 	LREP
						frecuencia = ""
						asignacion = ""

						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"

						# Se registra el concepto 502

						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = x.monto
						asignacion  = asignacion
						deduc       = float(operador)
						deduccion   = "%.2f" % round(deduc,2)
						asig_deduc  =  x.id
						filtro      = "2"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			elif str(x.codigo) == "148":

				if str(x.emp.clas_personal) != "Obrero":
					raise osv.except_osv(_("Warning!"), _("Disculpe este concepto solo es asignado al personal (Obrero)..."))

				elif not data_asig_deduc['cant_dias']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la cantidad de dias..."))
				else:
					get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

					search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
					employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
					cod = ""
					for i in employee_cod:
						cod = i['cod']

					if cod == x.codigo:
						self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
					else:

						sm = float(x.sueldo)

						operador   = sm/int(x.cant_dias)*1.5 # Concepto 148, Domingo y feriados laborados
						frecuencia = ""
						deduccion = ""

						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"

						# Se registra el concepto 148

						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						deduccion   = deduccion
						asig       = float(operador)
						asignacion   = "%.2f" % round(asig,2)
						asig_deduc  =  x.id
						filtro      = "2"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
			
			elif str(x.codigo) == "243":
				
				get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('cedula','=',x.cedula)], context=None) # Se busca el ID dado
				employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
	
				search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				cod = ""
				for i in employee_cod:
					cod = i['cod']
					#print "REGISTRO: "+str(i['cod'])
				
				if cod == x.codigo:
					
					#raise osv.except_osv(_("Warning!"), _("El concepto "+"("+i['cod']+")"+" "+i['descripcion']+" ya esta asignado, intente de nuevo..."))
					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:
					if not data_asig_deduc['monto']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el monto..."))
					
					if int(employee[0]['prima_responsabilidad']) == 2 or str(employee[0]['prima_responsabilidad']) == "False":
	
						raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no contiene prima de responsabilidad..."))
					else:
						monto      = x.monto # Concepto 243
						operador   = monto # Formula 104,243,107,208,181,210,249,168,154,303,304,305,306
						frecuencia = ""
						deduccion  = ""
						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"
						#print "FRECUENCIA: "+str(frecuencia)
						# Se registra el concepto 243 Prima de responsabilidad
	
						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						asig_deduc  =  x.id
						
						asig       = float(operador)
						asignacion  = "%.2f" % round(asig,2)
						filtro      = "1"
						nomina      = x.nomina_admin.id
						# Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
			
			elif str(x.codigo) == "181": # Concepto Prima por hijo (181)
				
				get_hr = self.pool.get('hr.employee') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('cedula','=',x.cedula)], context=None) # Se busca el ID dado
				employee = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
	
				search_get_hr = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
				cod = ""
				for i in employee_cod:
					cod = i['cod']
				if cod == x.codigo:
					
					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:
					for y in employee:
						familiar_id = y['familiar'] # Grupo de id de los familiares del empleado
						
					get_carga = self.pool.get('becado.carga.familiar') # Objeto hr_employee (Empleado)
					search_get_hr = get_carga.search(cr, uid, [('id','=',familiar_id),('parentesco','=','1')], context=None) # Se busca el ID dado
					carga = get_carga.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
					familiar = len(carga)
					if not carga:
						raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no dispone hijos como carga familiar..."))
					else:
						monto = 0
						for c in carga:
							monto += int(c['mount_hijo'])
							valor = monto

						if int(valor) == 0:
							raise osv.except_osv(_("Warning!"), _("Disculpe actualmente no dispone Prima por Hijos, intente de nuevo, o Contacte al Administrador del sitio..."))
						else:
							
							operador   = valor # Salida de los resultados del monto a pagar (181)
							frecuencia = ""
							deduccion  = ""
							if int(x.frecuencia) == 1:
								frecuencia = "F"
							elif int(x.frecuencia) == 2:
								frecuencia = "E"
							cedula      = x.cedula
							cod         = x.codigo
							frecuencia  = frecuencia
							descripcion =  x.consulta.concepto
							cantidad    = ""
							asig_deduc  =  x.id
							
							asig        = float(operador)
							asignacion  = "%.2f" % round(asig,2)
							filtro      = "1"
							nomina      = x.nomina_admin.id
							# Salida de los datos al modelo movimientos (hr.movement.payslip)
							self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)

			#########################################################################################
			elif str(x.codigo) == "590": # Concepto F.A.O.V (590)

				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)

				search_get_hr = get_hr.search(cr, uid, [('asig_deduc','=',x.id),('incidencia','=','si')], context=None) # Se busca el ID dado
				employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado

				search_get = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				register_id = get_hr.read(cr,uid,search_get,context=context) # Se refleja el resultado
				if not employee_cod:
					raise osv.except_osv(_("Warning!"), _("Disculpe no existe incidencias salariales, debe ingresar los conceptos que dependan del mismo para realizar el calculo (F.A.O.V)..."))
				else:
					cod = ""
					for i in register_id:
						cod = i['cod']
					if cod == x.codigo: # En caso de que exista, emita un mesaje de que ya el registro existe

						self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
					else:
						sum_incidencias = 0
						for i in employee_cod:
							cod = i['cod']
							sum_incidencias += float(i['asignacion']) # Sumatoria de los conceptos que tengan incidencias salariales
							result_incidencia = (float(sum_incidencias))*0.01 # Formula del concepto (590)s F.A.O.V Monto para fraccion de quincena
						monto = result_incidencia # Resultado de la operacion

						operador    = monto # Salida de los resultados del monto a pagar (181)
						frecuencia  = ""
						asignacion  = ""
						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"
						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						asig_deduc  =  x.id
						deduc       = float(operador)
						deduccion   = "%.2f" % round(deduc,2)
						filtro      = "2"
						nomina      = x.nomina_admin.id
						#Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
			elif str(x.codigo) == "183" or str(x.codigo) == "184": # Descanso laborado (183)

				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
				search_get = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				register_id = get_hr.read(cr,uid,search_get,context=context) # Se refleja el resultado

				cod = ""
				for i in register_id:
					cod = i['cod']
				if cod == x.codigo: # En caso de que exista, emita un mensaje de que ya el registro existe

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:	# Si es distinto a personal Obrero emita un mensaje de restriccion
					
					if not data_asig_deduc['cant_dias']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
					elif not data_asig_deduc['cant_horas']:
						raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
					else:
						if str(x.codigo) == "183":
							monto = float(x.sueldo)/int(x.cant_dias)*1*int(x.cant_horas) # Formula del concepto (183) Descanso Laborado
						else:
							monto = float(x.sueldo)/int(x.cant_dias)*1*int(x.cant_horas) # Formula del concepto (184) Permiso no remunerado
						operador    = monto # Salida de los resultados del monto a pagar (181)
						frecuencia  = ""
						deduccion   = ""
						if int(x.frecuencia) == 1:
							frecuencia = "F"
						elif int(x.frecuencia) == 2:
							frecuencia = "E"
						cedula      = x.cedula
						cod         = x.codigo
						frecuencia  = frecuencia
						descripcion =  x.consulta.concepto
						cantidad    = ""
						asig_deduc  =  x.id
						asig        = float(operador)
						asignacion  = "%.2f" % round(asig,2)
						filtro      = "1"
						nomina      = x.nomina_admin.id
						#Salida de los datos al modelo movimientos (hr.movement.payslip)
						self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
			
			elif str(x.codigo) == "149": # Bono nocturno (149) Asignacion de bono nocturno mensual
				get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_movement_payslip (Empleado)
				search_get = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc','=',x.id)], context=None) # Se busca el ID dado
				register_id = get_hr.read(cr,uid,search_get,context=context) # Se refleja el resultado

				cod = ""
				for i in register_id: # iteramos, comprobando si el registro existe
					cod = i['cod']
				if cod == x.codigo: # En caso de que exista, emita un mensaje de que ya el registro existe

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:

					if str(x.emp.clas_personal) !="Obrero":
						raise osv.except_osv(_("Warning!"), _("Disculpe el bono vacacional solo es asignado al personal Obrero..."))
					else:
						fecha_actual = date.today() # Fecha actual d/m/Y
						ano_actual = fecha_actual.year # Se optiene el año actual
						mes_actual = fecha_actual.month # Se optiene el mes actual
						dia_actual = fecha_actual.day # Se optiene el dia actual

						if not data_asig_deduc['cant_dias']:
							raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
						elif not data_asig_deduc['cant_horas']:
							raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar el valor..."))
						else:
							if int(dia_actual) < 16:
								raise osv.except_osv(_("Warning!"), _("Disculpe el bono vacacional es asignado mensualmente..."))
							else:
								sm    = float(x.sueldo)
								dias1 = int(x.cant_dias)
								dias2 = int(x.cant_horas)
								monto = ((sm/dias1/int(7))*0.3)*dias2

								operador    = monto # Salida de los resultados del monto a pagar (181)
								frecuencia  = ""
								deduccion   = ""
								if int(x.frecuencia) == 1:
									frecuencia = "F"
								elif int(x.frecuencia) == 2:
									frecuencia = "E"
								cedula      = x.cedula
								cod         = x.codigo
								frecuencia  = frecuencia
								descripcion =  x.consulta.concepto
								cantidad    = ""
								asig_deduc  =  x.id
								asig        = float(operador)
								asignacion  = "%.2f" % round(asig,2)
								filtro      = "1"
								nomina      = x.nomina_admin.id
								#Salida de los datos al modelo movimientos (hr.movement.payslip)
								self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro, nomina,context)
			#########################################################################################
			elif str(x.codigo) == "126" or str(x.codigo) == "142": # Bono vacacional (126)
				get_hr = self.pool.get('hr.movement.payslip.vacaciones') # Objeto hr_movement_payslip (Empleado)
				search_get = get_hr.search(cr, uid, [('cod','=',x.codigo),('asig_deduc_vac','=',x.id)], context=None) # Se busca el ID dado
				register_id = get_hr.read(cr,uid,search_get,context=context) # Se refleja el resultado

				cod = ""
				for i in register_id: # iteramos, comprobando si el registro existe
					cod = i['cod']
				if cod == x.codigo: # En caso de que exista, emita un mensaje de que ya el registro existe

					self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':'1'}, context=context) # Reseteo los valores a vacio
				else:
					if str(x.nomina_admin.tipo_nomina) !="Vacaciones": # NOmina de vacaciones
						raise osv.except_osv(_("Warning!"), _("Disculpe el concepto "+str(x.consulta.concepto)+" no corresponde a la nomina Regular, intente de nuevo..."))
					else:
						get_hr = self.pool.get('hr.movement.payslip') # Objeto hr_employee (Empleado)
	
						search_get_hr = get_hr.search(cr, uid, [('asig_deduc','=',x.id),('incidencia','=','si')], context=None) # Se busca el ID dado
						employee_cod = get_hr.read(cr,uid,search_get_hr,context=context) # Se refleja el resultado
						sum_incidencias   = 0
						result_incidencia = 0
						for i in employee_cod:
							cod = i['cod']
							sum_incidencias += float(i['asignacion']) # Sumatoria de los conceptos que tengan incidencias a excepcion del mismo concepto a calcular
							result_incidencia = float(sum_incidencias)
						if int(result_incidencia) == 0:
							raise osv.except_osv(_("Warning!"), _("Disculpe debe disponer de algun concepto, intente de nuevo..."))
						else:
							incidencias = result_incidencia # Resultado de la operacion
							###############################################
							#         	Salario diario
							###############################################
							sm           = float(x.sueldo) # Sueldo mensual
							diario       = sm / int(30) # Monto diario
							#Realizar consulta sobre otras remuneraciones
							print "INCIDENCIAS: "+str(incidencias)
							remuneracion = float(incidencias) / int(30) # Otras remuneraciones
							AL_BFA       = (sm/int(30))*int(95)/int(360) # Alicuota Bono fin de ano
							total_diario = float(diario) + float(remuneracion) + float(AL_BFA)# Total diario

							print "SUELDO DIARIO: "+str(diario)
							print "SUELDO OTRAS REMUNERACIONES: "+str(remuneracion)
							print "ALICUOTA BONO FIN DE ANO: "+str(AL_BFA)
							print "TOTAL DIARIO: "+str(total_diario)
							###############################################
							#	  Bono vacacional empleados
							###############################################
							if str(x.emp.clas_personal) == "Empleado Fijo" or str(x.emp.clas_personal) == "Directivo":
								if str(x.consulta.concepto) == "Bono vacacional":
									dias_corres    = int(45) # Dias corresponden a empleados
								else: # Bono post vacacional para el personal empleado
									dias_corres    = int(18) # Dias corresponden a empleados
								operacion_bono = dias_corres * total_diario # Asignacion Bono Vacacional para el pesonal empleado
								print "BONO VACACIONAL EMPLEADOS: "+str(operacion_bono)
								###############################################
								#        Bono Post vacacional empleados
								###############################################
								#dias_corres_post    = int(18)
								#operacion_bono_post = dias_corres_post * total_diario
								#print "BONO POST VACACIONAL EMPLEADOS: "+str(operacion_bono_post)
								operador    = operacion_bono # Salida de los resultados del monto a pagar (181)
								frecuencia  = ""
								deduccion   = ""
								if int(x.frecuencia) == 1:
									frecuencia = "F"
								elif int(x.frecuencia) == 2:
									frecuencia = "E"
								cedula      = x.cedula
								cod         = x.codigo
								frecuencia  = frecuencia
								descripcion =  x.consulta.concepto
								cantidad    = ""
								asig_deduc  =  x.id
								asig        = float(operador)
								asignacion  = "%.2f" % round(asig,2)
								filtro      = "1"
								nomina      = x.nomina_admin.id
								#Salida de los datos al modelo movimientos (hr.movement.payslip)
								self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
							elif str(x.emp.clas_personal) == "Obrero": # Personal Obrero Bono vacacional y Post vacacional
								#print "Accion obrero"
								if str(x.consulta.concepto) == "Bono vacacional":
									dias_corres    = int(50) # Dias corresponden a empleados
								else: # Bono post vacacional para el personal empleado
									dias_corres    = int(30) # Dias corresponden a empleados
								operacion_bono = dias_corres * total_diario # Asignacion Bono Vacacional para el pesonal empleado
								print "BONO VACACIONAL OBRERO: "+str(operacion_bono)
								###############################################
								#        Bono Post vacacional empleados
								###############################################
								#dias_corres_post    = int(18)
								#operacion_bono_post = dias_corres_post * total_diario
								#print "BONO POST VACACIONAL EMPLEADOS: "+str(operacion_bono_post)
								operador    = operacion_bono # Salida de los resultados del monto a pagar (181)
								frecuencia  = ""
								deduccion   = ""
								if int(x.frecuencia) == 1:
									frecuencia = "F"
								elif int(x.frecuencia) == 2:
									frecuencia = "E"
								cedula      = x.cedula
								cod         = x.codigo
								frecuencia  = frecuencia
								descripcion =  x.consulta.concepto
								cantidad    = ""
								asig_deduc  =  x.id
								asig        = float(operador)
								asignacion  = "%.2f" % round(asig,2)
								filtro      = "1"
								nomina      = x.nomina_admin.id
								#Salida de los datos al modelo movimientos (hr.movement.payslip)
								self.save_concepts(cr,uid,ids,cedula,cod,frecuencia,descripcion,cantidad,asignacion,deduccion,asig_deduc,filtro,nomina,context)
	#########################################################################################################
	#Metodo global para guardar los conceptos Asignacion/ Deduccion, segun los conceptos asignados
	#########################################################################################################
	def save_concepts(self, cr, uid, ids, ced, cod, fre, descr, can, asig, deduc, id_model, filtro, nomina, context):
		# Se registra los conceptos en hr.movement.payslip Asignacion/Deduccion
		# Proceso condicional para establecer los conceptos que tengan incidencias salariales
		browse_data = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)
		for i in browse_data:
			nomina = i.nomina_admin.tipo_nomina

			if str(cod) == "502" or str(cod) == "561" or str(cod) == "514" or str(cod) == "562":
				cantidad_d = i.monto
				cantidad_h = ""
			else:
				cantidad_d = i.cant_dias
				cantidad_h = i.cant_horas

			if str(nomina) == "Regular":
				relacion = 'asig_deduc' # Relacion a nomina Regular
				modelo = 'hr.movement.payslip' # Modelo relacional
			elif str(nomina) == "Vacaciones":
				relacion = 'asig_deduc_vac' # Relacion a nomina de Vacaciones
				modelo = 'hr.movement.payslip.vacaciones' # modelo Relacional

		if str(cod) == "008" or str(cod) == "009" or str(cod) == "101" or str(cod) == "125" or str(cod) == "104" or str(cod) == "243" or str(cod) == "107" or str(cod) == "116" or str(cod) == "208" or str(cod) == "181" or str(cod) == "210" or str(cod) == "126" or str(cod) == "142" or str(cod) == "134" or str(cod) == "148" or str(cod) == "143" or str(cod) == "149" or str(cod) == "150" or str(cod) == "151" or str(cod) == "249" or str(cod) == "168" or str(cod) == "154" or str(cod) == "456" or str(cod) == "102" or str(cod) == "182" or str(cod) == "462" or str(cod) == "126" or str(cod) == "142":
			incidencia = "si"
		else:
			incidencia = "no"

		id_att = self.pool.get(modelo).create(cr, uid, {
			'cedula': ced,
			'cod': cod,
			'frecuencia': fre,
			'descripcion': descr,
			'cantidad_d': cantidad_d,
			'cantidad_h': cantidad_h,
			'asignacion': asig, # redondeo la sifra a dos decimales
			'deduccion': deduc,
			relacion: id_model,
			'filtro': filtro,
			'incidencia': incidencia,
			'tipo_nomina':nomina,
			'item':"1",
			}, context=context)
		self.write(cr, uid, ids, {'accion': '1'}, context=context) # Campo de accion
		self.write(cr, uid, ids, {'codigo': '','consulta':'','frecuencia':'','formula':'','cant_dias':'','cant_horas':'','monto':'','filtro':''}, context=context) # Reseteo los valores a vacio
		self.buscar(cr, uid, ids, context)
		self.promediar_calculo(cr, uid, ids, context) # Llamada al proceso de recalculo de asignaciones y deducciones

		return id_att

	def search_concepto(self, cr, uid, ids, argument_search, item, context=None):

		values = {}
		mensaje = {}

		if not argument_search:

			return values
		obj_dp = self.pool.get('hr.concepts')
		
		if item == "1":

			#======================== Busqueda por codigo ============================
			search_job_id = obj_dp.search(cr, uid, [('codigo','=',argument_search)])

			datos_job_id = obj_dp.read(cr,uid,search_job_id,context=context)
			#========================================================================
			if not datos_job_id:

				mensaje = {
					'title'   : "Advertencia",
					'message' : "Disculpe el concepto no existe, intente de nuevo...",
				}
				values.update({'codigo' : None,})
			elif datos_job_id:

				values.update({
					'consulta' : datos_job_id[0]['id'],
					'frecuencia' : datos_job_id[0]['frecuencia'],
					'formula' : datos_job_id[0]['formula'],
					})
		elif item == "2":

			#======================== Busqueda por descripcion ======================
			search_job_id = obj_dp.search(cr, uid, [('id','=',argument_search)])

			datos_job_id = obj_dp.read(cr,uid,search_job_id,context=context)
			#========================================================================
			if not datos_job_id:

				mensaje = {
					'title'   : "Advertencia",
					'message' : "Disculpe el concepto no existe, intente de nuevo...",
				}
				values.update({'codigo' : None,})
			elif datos_job_id:
				values.update({
					'codigo' : datos_job_id[0]['codigo'],
					'frecuencia' : datos_job_id[0]['frecuencia'],
					'formula' : datos_job_id[0]['formula'],
					})
		return {'value' : values,'warning' : mensaje}

	#################################################################################################

	_columns = {
            'cedula': fields.char(string = "Cedula", size = 10, required = True),
            'nombres': fields.char(string = "Nombres / Apellidos", size = 150, required = False),
            'date_ingreso': fields.date(string = "Fecha de ingreso", required = False),
            'date_egreso': fields.date(string = "Fecha de egreso", required = False),
            'ano_servicio': fields.char(string = "Años de servicio", size = 25, required = False),
            'status' : fields.selection((('1','Activo'),('2','Peri?do de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
            'charge_acterior': fields.many2one("hr.job", "Cargo", required = False),
            'sueldo': fields.char(string = "Sueldo Bs", size = 10, required = False),
            'dep_lab' : fields.many2one("hr.department", "Departamento", required = False),
	    'emp' : fields.many2one("becados.clasper", "Empleado", required = False),
            'movement_ids' : fields.one2many("hr.movement.payslip","asig_deduc",string="Asignaciones / deducciones"),
	    'vacaciones_ids' : fields.one2many("hr.movement.payslip.vacaciones","asig_deduc_vac",string="Asignaciones / deducciones"),
	    'monto_c': fields.char(string = "Monto a cobrar (Empleado)", size = 10, required = False),
	    'monto_c_vac': fields.char(string = "Monto a cobrar (Empleado)", size = 10, required = False),
	    'monto_asignacion': fields.char(string = "Monto asignacion", size = 10, required = False),
	    'monto_asignacion_vac': fields.char(string = "Monto asignacion", size = 10, required = False),
	    'monto_deduccion': fields.char(string = "Monto deduccion", size = 10, required = False),
	    'monto_deduccion_vac': fields.char(string = "Monto deduccion", size = 10, required = False),
	    'nomina_admin' : fields.many2one("becados.tiponomina", "Nómina Administrativa", required = True),
	    'image' : fields.binary("",help="Empleado"),
	    'codigo': fields.char(string = "Código", size = 10, required = False),
	    'consulta' : fields.many2one("hr.concepts", "Consulta", required = False),
	    'frecuencia' : fields.selection((('1','Fijo'),('2','Esporádico'),('3','Prestamo'),('4','Acumulado')), "Frecuencia", required=False),
	    'monto': fields.char(string = "Monto en Bs", size = 10, required = False),
	    'formula': fields.char(string ="Fórmula", size = 256, required = False),
	    'cant_horas': fields.char(string ="Cant/Horas", size = 10, required = False),
	    'cant_dias': fields.char(string ="Cant/Dias", size = 10, required = False),
	    'codigo_delete': fields.char(string ="Código", size = 10, required = False),
	    'codigo_delete_vac': fields.char(string ="Código", size = 10, required = False),
	    'filtro': fields.char(string = "", size = 10, required = False),
	    'accion': fields.char(string = "", size = 10, required = False), # Elemento de accion
	    'tree_id' : fields.selection((('1','Regular'),('2','Bono fin de año'),('3','Vacaciones'),('4','Juguetes')), "Nomina", required=False),
	    'state' : fields.selection([('1','Activo'),('5','Suspendido'),('7','Egresado'),('6','Vacaciones'),('3','Reposo Médico')], string="Estado"),
	}

	_defaults = {
		'state':'1',
	}

def redondear(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida