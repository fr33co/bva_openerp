# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import os
from openerp.tools.translate import _
from openerp.osv import fields, osv
import base64#Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring#Necesario para la generación del .xsl
#~ from fpdf import FPDF
#~ import fpdf
import res_concept
import res_nom
import nom_detallado
import pdf_nominas
import xlwt
import unicodedata

class NominaBecados(osv.Model):
	
	_name = 'becados.nomina'
	
	_rec_name = 'anyo'
	
	#Función para pasar a estado de Pre-nómina----------------------------------------------
	def action_prenomina(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'prenomina'}, context=context)
		
	#Función para pasar a estado de Nómina-------------------------------------------------------------------------------------------
	def action_nomina(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'nomina'}, context=context)
		
	#Función para pasar a estado de Cierre de Nómina---------------------------------------------------------------------------------
	def action_cierre(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'cierre'}, context=context)
		
	#Función para pasar a estado de Cancelado----------------------------------------------------------------------------------------
	def action_cancelar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'cancelado'}, context=context)
	
	#Función para leer el tipo de beca de la nómina actual---------------------------------------------------------------------------
	def get_tipo_beca(self, cr, uid, ids, context):
		nomina = self.browse(cr, uid, ids, context=None)
		for campos in nomina:
			tipo_beca = campos.tipo_beca
		return str(tipo_beca)	
	
	#Función para leer el banco de la nómina actual----------------------------------------------------------------------------------
	def get_banco(self, cr, uid, ids, context):
		nomina = self.browse(cr, uid, ids, context=None)
		for campos in nomina:
			banco = campos.banco
		return str(banco)
	
	
	#Función para pasar a estado de Cancelado----------------------------------------------------------------------------------------
	def generar_nominas(self, cr, uid, ids, context=None):
		
		obj_proceso_nomina = self.pool.get('becados.nominaindividual')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar los campos necesarios
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			anyo = x_browse_id.anyo
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina #Leer el tipo de nómina de la nómina actual
			tiponominaletras = x_browse_id.tipo_nomina.tipo_nomina
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			#~ print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			#~ print "mes de la pre-nómina: "+str(mes)+"\n"
			#~ print "Stage de la pre-nómina: "+str(stage)+"\n"
			
			for becado in x_browse_id.becados:#Recorrer los registros dentro del campo 'becados' del modelo de Nómina
				cedula = becado.cedula
				name = becado.name_related
				tipo_beca = becado.tipo_beca.id
				status = becado.status
				#Definir el monto de la asignación para los becados según el tipo de nómina (en letras) escogido
				if tiponominaletras == "Regular":
					monto = becado.tipo_beca.asignacion
				else:
					monto = becado.tipo_beca.asignacion*4
					
				#Definir tipo de asignación para los becados según el tipo de nómina (en letras) escogido
				if tiponominaletras == "Regular":
					tipo_asig = "beca_completa"
				else:
					tipo_asig = "bono_f"
				
				if status == "5":
					tipo_asig = "sin_asignacion"
					monto = float(0)
				
				#~ print cedula + " " + name + " " + str(tipo_beca)
				
				#Preparación de los datos compuestos
				codigo = str(mes)+str(anyo)+str(cedula)
								
				#Verificamos si la nómina individual del becado ya fue generada (se toma en cuenta el código)
				search_nomina1 = obj_proceso_nomina.search(cr, uid, [('codigo','=',codigo)], count=False)
				
				if not search_nomina1: #Verificar esto, al parecer impide que se listen algunas nóminas individuales 
				
					id_att = obj_proceso_nomina.create(cr, uid, {
						'nomina': id_nomina, 
						'codigo': codigo,
						'becado': becado.id,
						'anyo': anyo,
						'mes': mes,
						'tipo_beca': tipo_beca,
						'asignacion' : tipo_asig,
						'monto': monto,
						}, context=context)
				
				else:
					print "La nómina ya existe..."
					#raise osv.except_osv(_("Warning!"), _("La nómina ya existe..."))
			
			#~ print "\n"
			#Ahora verificamos si las nóminas individuales se corresponden con la lista de becados seleccionados.
			#Si alguna de éllas no pertenece a ningún becado de la lista, procedemos a eliminarla de la lista de nóminas
			for nomina in x_browse_id.nomina_individual:
				#~ print nomina.codigo	+ " " + nomina.becado.cedula
				contador = 0 #Contador para validar si la nómina pertenece a algún becado seleccionado
				for becado2 in x_browse_id.becados:
					#~ print ""+becado2.cedula
					if becado2.cedula == nomina.becado.cedula:
						#~ print becado2.cedula+"=="+nomina.becado.cedula
						contador = contador + 1
					else:
						contador = contador 
				#~ print contador
				#~ print nomina.id
				
				if contador <= 0:
					try:
						obj_proceso_nomina.unlink(cr, uid, nomina.id, context=None)
						# Revisar: Hasta los momentos se actualiza la lista de nóminas individuales según el número de becados, 
						#pero ocurre un error si no se ha guardado la nómina después de borrar un becado de la lista y se intenta generar de nuevo la nómina.
					except:
						nomina

	#Función para la generación de los reportes .txt y xsl de la pre-nómina----------------------------------------------------------	
	def action_archivar_prenomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			banco = x_browse_id.banco.banco #Leer el banco de la nómina actual
			tipobeca = x_browse_id.tipo_beca.tipo_beca #Leer el tipo de beca de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual 
			#~ print "Id de la nómina: "+str(id_nomina)+"\n"
			#~ print "mes de la nómina: "+str(mes)+"\n"
			#~ print "Stage de la nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
		
			if search_nomina1 > 0:
				#~ print str(search_nomina1)+"\n"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros tomando en cuenta sólo el campo de asignación para el cálculo del monto a debitar al titular de la cuenta (Gobernación)
						cuenta_gob = "0102021598000631633285"
						monto_deb = 0
						for registro in nomina.nomina_individual:
							monto_deb = monto_deb + int(registro.monto)
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						
						anyo = time.strftime('%Y')
						banc = "VZLA"
						if 'ESPECIAL' in tipobeca:
							t_beca = 'ESPECIAL'
						else:
							t_beca = self.elimina_tildes(tipobeca.upper())
						#Se construye la cabecera o título en base al banco, el año y el tipo de beca
						cabecera = "TXT." + banc + "." + t_beca + "-" + mes.upper() + "-" + anyo + "\n"
						
						data = cabecera.rjust(65) + "HGOBERNACION DEL ESTADO ARAGUA           "+cuenta_gob+str(time.strftime("%d/%m/%y"),)+str(monto_deb).zfill(11)+"00"+"03291\n\n"
						data1 = []
						for becado in nomina.nomina_individual:
							if not becado.becado.numero_cuenta:
								cuenta = ""
							else:
								cuenta = str(becado.becado.numero_cuenta)
							if not becado.monto:
								asign = ""
							else:
								asign = int(becado.monto)
							primer_nombre = self.elimina_tildes(becado.becado.primer_nombre.strip().upper())
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
							else:
								segundo_nombre = self.elimina_tildes(becado.becado.segundo_nombre[0].upper())
							primer_apellido = self.elimina_tildes(becado.becado.primer_apellido.strip().upper())
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
							else:
								segundo_apellido = self.elimina_tildes(becado.becado.segundo_apellido[0].upper())
							if not becado.becado.tipo_cuenta:
								tipo_cuenta = ""
							else:
								tipo_cuenta = becado.becado.tipo_cuenta
							if not becado.becado.cedula:
								cedula = ""
							else:
								cedula = str(becado.becado.cedula).zfill(10)+"0" #Con zfill completamos la cédula con ceros a la izquierda hasta contar 10 dígitos en este caso 
							cod_stand = "03291"
							ced_cod_stand = cedula+cod_stand
							cod_stand2 = "770"
							
							part_1 = tipo_cuenta.ljust(0)+cuenta.ljust(0)+str(asign).zfill(9).ljust(0)+"00".ljust(0)+tipo_cuenta.ljust(0)+cod_stand2.ljust(0)
							part_2 = primer_apellido+" "+segundo_apellido+" "+primer_nombre+" "+segundo_nombre
							
							part_2 = part_2.ljust(40)
							
							part_3 = ced_cod_stand.rjust(5)
							
							datos = part_1+part_2+part_3+"\n\n"
							
							datos1 = []
							datos1.append(becado.becado.cedula)
							#~ datos1.append(str(becado.becado.name_related.encode("utf-8")))
							datos1.append(self.elimina_tildes(becado.becado.primer_apellido.upper()))
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
								datos1.append(segundo_apellido)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_apellido.upper()))
							datos1.append(self.elimina_tildes(becado.becado.primer_nombre.upper()))
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
								datos1.append(segundo_nombre)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_nombre.upper()))
							if not becado.monto:
								m = ""
								datos1.append(m) 
							else:
								datos1.append(becado.monto)
							if not becado.becado.numero_cuenta:
								num_c = ""
								datos1.append(num_c)
							else:
								datos1.append(becado.becado.numero_cuenta)
							if not becado.becado.entidad_bancaria:
								ent_banc = ""
								datos1.append(ent_banc)
							else:
								datos1.append(self.elimina_tildes(becado.becado.entidad_bancaria.banco.upper()))
							f_nac = ""
							datos1.append(f_nac)
							datos1.append("BECADO")
							datos1.append(self.elimina_tildes(becado.becado.direccion.upper()))
							datos1.append(becado.becado.tlf_movil)
							datos1.append(becado.becado.status)
							if not becado.becado.fecha_ingreso:
								f_ingreso = ""
								datos1.append(f_ingreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_ingreso))
							if not becado.becado.fecha_egreso:
								f_egreso = ""
								datos1.append(f_egreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_egreso))
							if not becado.tipo_beca:
								t_b_i = ""
								cod_beca = ""
								cod_t_beca = ""
								t_b_n = ""
								datos1.append(t_b_i)
								datos1.append(cod_beca)
								datos1.append(cod_t_beca)
								datos1.append(t_b_n)
							else:
								datos1.append(becado.tipo_beca.id)
								datos1.append(becado.tipo_beca.cod_beca)
								datos1.append(becado.tipo_beca.cod_t_beca)
								datos1.append(becado.tipo_beca.tipo_beca.upper())
							if not becado.becado.sede.descripcion:
								desc_sede = ""
								datos1.append(desc_sede)
							else:
								datos1.append(self.elimina_tildes(becado.becado.sede.descripcion.upper()))
							if not becado.becado.grado_instruccion:
								grado_i = ""
								datos1.append(grado_i)
							else:
								datos1.append(self.elimina_tildes(becado.becado.grado_instruccion.grado_instruc))
							if not becado.becado.camisa:
								b_camisa = ""
								datos1.append(b_camisa)
							else:
								datos1.append(becado.becado.camisa)
							if not becado.becado.pantalon:
								b_pantalon = ""
								datos1.append(b_pantalon)
							else:
								datos1.append(becado.becado.pantalon)
							if not becado.becado.zapato:
								b_zapato = ""
								datos1.append(b_zapato)
							else:
								datos1.append(becado.becado.zapato)
							if not becado.becado.sexo:
								b_sexo = ""
								datos1.append(b_sexo)
							else:
								datos1.append(becado.becado.sexo)
							if not becado.becado.edad:
								b_edad = ""
								datos1.append(b_edad)
							else:
								datos1.append(becado.becado.edad)
							
							if becado.becado.entidad_bancaria.banco == "Venezuela" and becado.becado.status == '1':
								data = data + datos
							data1.append(datos1)
							
						#~ print data
						#~ print datos1
						
						
					#Ejecutamos el método de registro del txt 
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, tipobeca, mes, data, stage, context)
					
					#Ejecutamos el método de generación de reportes en PDF
					gen_pdf = self.generar_pdf(cr, uid, ids, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
					
					#Ejecutamos el método de generación de reportes en XLS
					gen_xls = self.generar_xls(cr, uid, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
			
			else:
				print "No se encontró ningún registro"
				
		
	#Función para la generación de los reportes .txt y xsl de la nómina--------------------------------------------------------------	
	def action_archivar_nomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			banco = x_browse_id.banco.banco #Leer el banco de la nómina actual
			tipobeca = x_browse_id.tipo_beca.tipo_beca #Leer el tipo de beca de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			#~ print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			#~ print "mes de la pre-nómina: "+str(mes)+"\n"
			#~ print "Stage de la pre-nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
			
			if search_nomina1 > 0:
				print str(search_nomina1)+"\n"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros tomando en cuenta sólo el campo de asignación para el cálculo del monto a debitar al titular de la cuenta (Gobernación)
						cuenta_gob = "0102021598000631633285"
						monto_deb = 0
						for registro in nomina.nomina_individual:
							monto_deb = monto_deb + int(registro.monto)
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						
						anyo = time.strftime('%Y')
						banc = "VZLA"
						if 'ESPECIAL' in tipobeca:
							t_beca = 'ESPECIAL'
						else:
							t_beca = self.elimina_tildes(tipobeca.upper())
						#Se construye la cabecera o título en base al banco, el año y el tipo de beca
						cabecera = "TXT." + banc + "." + t_beca + "-" + mes.upper() + "-" + anyo + "\n"
						
						data = cabecera.rjust(65) + "HGOBERNACION DEL ESTADO ARAGUA           "+cuenta_gob+str(time.strftime("%d/%m/%y"),)+str(monto_deb).zfill(11)+"00"+"03291\n\n"
						data1 = []
						for becado in nomina.nomina_individual:
							if not becado.becado.numero_cuenta:
								cuenta = ""
							else:
								cuenta = str(becado.becado.numero_cuenta)
							if not becado.monto:
								asign = ""
							else:
								asign = int(becado.monto)
							primer_nombre = self.elimina_tildes(becado.becado.primer_nombre.upper())
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
							else:
								segundo_nombre = self.elimina_tildes(becado.becado.segundo_nombre[0].upper())
							primer_apellido = self.elimina_tildes(becado.becado.primer_apellido.upper())
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
							else:
								segundo_apellido = self.elimina_tildes(becado.becado.segundo_apellido[0].upper())
							if not becado.becado.tipo_cuenta:
								tipo_cuenta = ""
							else:
								tipo_cuenta = becado.becado.tipo_cuenta
							if not becado.becado.cedula:
								cedula = ""
							else:
								cedula = str(becado.becado.cedula).zfill(10)+"0" #Con zfill completamos la cédula con ceros a la izquierda hasta contar 10 dígitos en este caso 
							cod_stand = "03291"
							ced_cod_stand = cedula+cod_stand
							cod_stand2 = "770"
							
							part_1 = tipo_cuenta.ljust(0)+cuenta.ljust(0)+str(asign).zfill(9).ljust(0)+"00".ljust(0)+tipo_cuenta.ljust(0)+cod_stand2.ljust(0)
							part_2 = primer_apellido+" "+segundo_apellido+" "+primer_nombre+" "+segundo_nombre
							
							part_2 = part_2.ljust(40)
							
							part_3 = ced_cod_stand.rjust(5)
							
							datos = part_1+part_2+part_3+"\n\n"
							
							datos1 = []
							datos1.append(becado.becado.cedula)
							#~ datos1.append(str(becado.becado.name_related.encode("utf-8")))
							datos1.append(self.elimina_tildes(becado.becado.primer_apellido.upper()))
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
								datos1.append(segundo_apellido)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_apellido.upper()))
							datos1.append(self.elimina_tildes(becado.becado.primer_nombre.upper()))
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
								datos1.append(segundo_nombre)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_nombre.upper()))
							if not becado.monto:
								m = ""
								datos1.append(m) 
							else:
								datos1.append(becado.monto)
							if not becado.becado.numero_cuenta:
								num_c = ""
								datos1.append(num_c)
							else:
								datos1.append(becado.becado.numero_cuenta)
							if not becado.becado.entidad_bancaria:
								ent_banc = ""
								datos1.append(ent_banc)
							else:
								datos1.append(self.elimina_tildes(becado.becado.entidad_bancaria.banco.upper()))
							if not becado.becado.fecha_nacimiento:
								f_nac = ""
								datos1.append(f_nac)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_nacimiento))
							datos1.append("BECADO")
							datos1.append(self.elimina_tildes(becado.becado.direccion.upper()))
							datos1.append(becado.becado.tlf_movil)
							datos1.append(becado.becado.status)
							if not becado.becado.fecha_ingreso:
								f_ingreso = ""
								datos1.append(f_ingreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_ingreso))
							if not becado.becado.fecha_egreso:
								f_egreso = ""
								datos1.append(f_egreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_egreso))
							if not becado.tipo_beca:
								t_b_i = ""
								cod_beca = ""
								cod_t_beca = ""
								t_b_n = ""
								datos1.append(t_b_i)
								datos1.append(cod_beca)
								datos1.append(cod_t_beca)
								datos1.append(t_b_n)
							else:
								datos1.append(becado.tipo_beca.id)
								datos1.append(becado.tipo_beca.cod_beca)
								datos1.append(becado.tipo_beca.cod_t_beca)
								datos1.append(becado.tipo_beca.tipo_beca.upper())
							if not becado.becado.sede.descripcion:
								desc_sede = ""
								datos1.append(desc_sede)
							else:
								datos1.append(self.elimina_tildes(becado.becado.sede.descripcion.upper()))
							if not becado.becado.grado_instruccion:
								grado_i = ""
								datos1.append(grado_i)
							else:
								datos1.append(self.elimina_tildes(becado.becado.grado_instruccion.grado_instruc))
							if not becado.becado.camisa:
								b_camisa = ""
								datos1.append(b_camisa)
							else:
								datos1.append(becado.becado.camisa)
							if not becado.becado.pantalon:
								b_pantalon = ""
								datos1.append(b_pantalon)
							else:
								datos1.append(becado.becado.pantalon)
							if not becado.becado.zapato:
								b_zapato = ""
								datos1.append(b_zapato)
							else:
								datos1.append(becado.becado.zapato)
							if not becado.becado.sexo:
								b_sexo = ""
								datos1.append(b_sexo)
							else:
								datos1.append(becado.becado.sexo)
							if not becado.becado.edad:
								b_edad = ""
								datos1.append(b_edad)
							else:
								datos1.append(becado.becado.edad)
							
							if becado.becado.entidad_bancaria.banco == "Venezuela" and becado.becado.status == '1':
								data = data + datos
							data1.append(datos1)
							
						#~ print data
						#~ print datos1
						
						
					#Ejecutamos el método de registro del txt 
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, tipobeca, mes, data, stage, context)
					
					#Ejecutamos el método de generación de reportes en PDF
					gen_pdf = self.generar_pdf(cr, uid, ids, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
					
					#Ejecutamos el método de generación de reportes en XLS
					gen_xls = self.generar_xls(cr, uid, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
					
			else:
				print "No se encontró ningún registro"
				
					
	#Función para la generación de los reportes .txt y xsl del cierre de nómina------------------------------------------------------
	def action_archivar_cierre(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			banco = x_browse_id.banco.banco #Leer el banco de la nómina actual
			tipobeca = x_browse_id.tipo_beca.tipo_beca #Leer el tipo de beca de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			#~ print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			#~ print "mes de la pre-nómina: "+str(mes)+"\n"
			#~ print "Stage de la pre-nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
			
			if search_nomina1 > 0:
				#~ print str(search_nomina1)+"\n"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros tomando en cuenta sólo el campo de asignación para el cálculo del monto a debitar al titular de la cuenta (Gobernación)
						cuenta_gob = "0102021598000631633285"
						monto_deb = 0
						for registro in nomina.nomina_individual:
							monto_deb = monto_deb + int(registro.monto)
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						
						anyo = time.strftime('%Y')
						banc = "VZLA"
						if 'ESPECIAL' in tipobeca:
							t_beca = 'ESPECIAL'
						else:
							t_beca = self.elimina_tildes(tipobeca.upper())
						#Se construye la cabecera o título en base al banco, el año y el tipo de beca
						cabecera = "TXT." + banc + "." + t_beca + "-" + mes.upper() + "-" + anyo + "\n"
						
						data = cabecera.rjust(65) + "HGOBERNACION DEL ESTADO ARAGUA           "+cuenta_gob+str(time.strftime("%d/%m/%y"),)+str(monto_deb).zfill(11)+"00"+"03291\n\n"
						data1 = []
						for becado in nomina.nomina_individual:
							if not becado.becado.numero_cuenta:
								cuenta = ""
							else:
								cuenta = str(becado.becado.numero_cuenta)
							if not becado.monto:
								asign = ""
							else:
								asign = int(becado.monto)
							primer_nombre = self.elimina_tildes(becado.becado.primer_nombre.upper())
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
							else:
								segundo_nombre = self.elimina_tildes(becado.becado.segundo_nombre[0].upper())
							primer_apellido = self.elimina_tildes(becado.becado.primer_apellido.upper())
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
							else:
								segundo_apellido = self.elimina_tildes(becado.becado.segundo_apellido[0].upper())
							if not becado.becado.tipo_cuenta:
								tipo_cuenta = ""
							else:
								tipo_cuenta = becado.becado.tipo_cuenta
							if not becado.becado.cedula:
								cedula = ""
							else:
								cedula = str(becado.becado.cedula).zfill(10)+"0" #Con zfill completamos la cédula con ceros a la izquierda hasta contar 10 dígitos en este caso 
							cod_stand = "03291"
							ced_cod_stand = cedula+cod_stand
							cod_stand2 = "770"
							
							part_1 = tipo_cuenta.ljust(0)+cuenta.ljust(0)+str(asign).zfill(9).ljust(0)+"00".ljust(0)+tipo_cuenta.ljust(0)+cod_stand2.ljust(0)
							part_2 = primer_apellido+" "+segundo_apellido+" "+primer_nombre+" "+segundo_nombre
							
							part_2 = part_2.ljust(40)
							
							part_3 = ced_cod_stand.rjust(5)
							
							datos = part_1+part_2+part_3+"\n\n"
							
							datos1 = []
							datos1.append(becado.becado.cedula)
							#~ datos1.append(str(becado.becado.name_related.encode("utf-8")))
							datos1.append(self.elimina_tildes(becado.becado.primer_apellido.upper()))
							if not becado.becado.segundo_apellido:
								segundo_apellido = ""
								datos1.append(segundo_apellido)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_apellido.upper()))
							datos1.append(self.elimina_tildes(becado.becado.primer_nombre.upper()))
							if not becado.becado.segundo_nombre:
								segundo_nombre = ""
								datos1.append(segundo_nombre)
							else:
								datos1.append(self.elimina_tildes(becado.becado.segundo_nombre.upper()))
							if not becado.monto:
								m = ""
								datos1.append(m) 
							else:
								datos1.append(becado.monto)
							if not becado.becado.numero_cuenta:
								num_c = ""
								datos1.append(num_c)
							else:
								datos1.append(becado.becado.numero_cuenta)
							if not becado.becado.entidad_bancaria:
								ent_banc = ""
								datos1.append(ent_banc)
							else:
								datos1.append(self.elimina_tildes(becado.becado.entidad_bancaria.banco.upper()))
							if not becado.becado.fecha_nacimiento:
								f_nac = ""
								datos1.append(f_nac)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_nacimiento))
							datos1.append("BECADO")
							datos1.append(self.elimina_tildes(becado.becado.direccion.upper()))
							datos1.append(becado.becado.tlf_movil)
							datos1.append(becado.becado.status)
							if not becado.becado.fecha_ingreso:
								f_ingreso = ""
								datos1.append(f_ingreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_ingreso))
							if not becado.becado.fecha_egreso:
								f_egreso = ""
								datos1.append(f_egreso)
							else:
								datos1.append(self.format_fecha(becado.becado.fecha_egreso))
							if not becado.tipo_beca:
								t_b_i = ""
								cod_beca = ""
								cod_t_beca = ""
								t_b_n = ""
								datos1.append(t_b_i)
								datos1.append(cod_beca)
								datos1.append(cod_t_beca)
								datos1.append(t_b_n)
							else:
								datos1.append(becado.tipo_beca.id)
								datos1.append(becado.tipo_beca.cod_beca)
								datos1.append(becado.tipo_beca.cod_t_beca)
								datos1.append(becado.tipo_beca.tipo_beca.upper())
							if not becado.becado.sede.descripcion:
								desc_sede = ""
								datos1.append(desc_sede)
							else:
								datos1.append(self.elimina_tildes(becado.becado.sede.descripcion.upper()))
							if not becado.becado.grado_instruccion:
								grado_i = ""
								datos1.append(grado_i)
							else:
								datos1.append(self.elimina_tildes(becado.becado.grado_instruccion.grado_instruc))
							if not becado.becado.camisa:
								b_camisa = ""
								datos1.append(b_camisa)
							else:
								datos1.append(becado.becado.camisa)
							if not becado.becado.pantalon:
								b_pantalon = ""
								datos1.append(b_pantalon)
							else:
								datos1.append(becado.becado.pantalon)
							if not becado.becado.zapato:
								b_zapato = ""
								datos1.append(b_zapato)
							else:
								datos1.append(becado.becado.zapato)
							if not becado.becado.sexo:
								b_sexo = ""
								datos1.append(b_sexo)
							else:
								datos1.append(becado.becado.sexo)
							if not becado.becado.edad:
								b_edad = ""
								datos1.append(b_edad)
							else:
								datos1.append(becado.becado.edad)
							
							if becado.becado.entidad_bancaria.banco == "Venezuela" and becado.becado.status == '1':
								data = data + datos
							data1.append(datos1)
							
						#~ print data
						#~ print datos1
						
						
					#Ejecutamos el método de registro del txt 
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, tipobeca, mes, data, stage, context)
					
					#Ejecutamos el método de generación de reportes en PDF
					gen_pdf = self.generar_pdf(cr, uid, ids, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
					
					#Ejecutamos el método de generación de reportes en XLS
					gen_xls = self.generar_xls(cr, uid, id_nomina, tiponomina, tipobeca, mes, data1, stage, context)
		
		else:
				print "No se encontró ningún registro"
				
				
	#Función para el registro de los archivos generados de la nómina-----------------------------------------------------------------
	def registro_archivo(self, cr, uid, nomina, tipo_nomina, tipo_beca, mes, data, stage, context):
		#Preparación de la descripción del tipo de beca
		if 'ESPECIAL' in tipo_beca:
			#~ cod_beca = '50'
			beca = 'BECA ESPECIAL'
		elif 'SOCIAL' in tipo_beca:
			#~ cod_beca = '10'
			beca = 'BECA SOCIAL'
		elif 'EXCELENCIA' in tipo_beca:
			#~ cod_beca = '10'
			beca = 'BECA EXCELENCIA'
		else:
			#~ cod_beca = '01'
			beca = 'BECA CYBERGUÍA'
				
		#Generación del nombre del reporte
		#~ fecha = time.strftime('(%d-%m-%y)')
		#~ dia = time.strftime('%d')
		anyo = time.strftime('%Y')
		#~ fecha = dia+"-"+mes+"-"+anyo
		nombre_archivo = "TXT.VZLA." + self.elimina_tildes(beca.decode("UTF-8").upper()) + "-" + mes.upper() + "-" + anyo +'.'+ 'txt'
		
		#Registro del .txt
		id_att = self.pool.get('ir.attachment').create(cr, uid, {
			'nomina': nomina, 
			'name': nombre_archivo,
			'stage': stage,
			'tipo_nomina': tipo_nomina,
			'tipo_beca': beca,
			'nombre': nombre_archivo,
			'res_name': nombre_archivo,
			'datas': base64.encodestring(data),
			'datas_fname': nombre_archivo,
			'res_model': 'becados.nomina',
			}, context=context)
		return id_att
		
		
	#Fucnión para la generación de reportes en PDF de la nómina
	def generar_pdf(self, cr, uid, ids, nomina, tipo_nomina, tipo_beca, mes, data1, stage, context):
		#Datos------------------------------------------------------------------
		id_nom = nomina
		nom = tipo_nomina
		
		#Preparación de la descripción del tipo de beca
		if 'ESPECIAL' in tipo_beca:
			#~ cod_beca = '50'
			beca = 'BECA ESPECIAL'
		elif 'SOCIAL' in tipo_beca:
			#~ cod_beca = '10'
			beca = 'BECA SOCIAL'
		elif 'EXCELENCIA' in tipo_beca:
			#~ cod_beca = '02'
			beca = 'BECA EXCELENCIA'
		else:
			#~ cod_beca = '01'
			beca = 'BECA CYBERGUÍA'
		
		#Captura del periodo de la nómina
		browse_id = self.browse(cr, uid, ids, context=None)
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			periodo_ini = self.format_fecha(x_browse_id.inicio_periodo) #Leer el periodo de inicio de la nómina
			periodo_fin = self.format_fecha(x_browse_id.fin_periodo) #Leer el periodo de fin de la nómina
		#Datos------------------------------------------------------------------
		
		#Opción a ejecutar------------------------------------------------------
		opc = ""

		if opc == 1:
			res_concept.gen_res_bank(cr, uid, id_nom, nom, periodo_ini, periodo_fin, tipo_beca, mes, stage, context)
		elif opc == 2:
			res_nom.gen_res_nom(cr, nom, periodo_ini, periodo_fin, tipo_beca, mes, data1)
		elif opc == 3:
			nom_detallado.gen_detallado(cr, uid, id_nom, nom, periodo_ini, periodo_fin, tipo_beca, mes, data1, stage, context)
		else:
			#Obtención de los valores retornados por la función que genera el archivo	de reporte de resumen de conceptos
			nom1, archivo1 = res_concept.gen_res_bank(cr, uid, id_nom, nom, periodo_ini, periodo_fin, tipo_beca, mes, data1, stage, context)
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'nomina': nomina, 
				'name': nom1,
				'stage': stage,
				'tipo_nomina': tipo_nomina,
				'tipo_beca': beca,
				'nombre': nom1,
				'res_name': nom1,
				'datas': base64.encodestring(archivo1.read()),
				'datas_fname': nom1,
				'res_model': 'becados.nomina',
				}, context=context)
				
				
			#Obtención de los valores retornados por la función que genera el archivo	de reporte de resumen de nomina	
			nom2, archivo2 = res_nom.gen_res_nom(cr, nom, periodo_ini, periodo_fin, tipo_beca, mes, data1)
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'nomina': nomina, 
				'name': nom2,
				'stage': stage,
				'tipo_nomina': tipo_nomina,
				'tipo_beca': beca,
				'nombre': nom2,
				'res_name': nom2,
				'datas': base64.encodestring(archivo2.read()),
				'datas_fname': nom2,
				'res_model': 'becados.nomina',
				}, context=context)
				
			
			#Obtención de los valores retornados por la función que genera el archivo	de reporte detallado
			nom3, archivo3 = nom_detallado.gen_detallado(cr, uid, id_nom, nom, periodo_ini, periodo_fin, tipo_beca, mes, data1, stage, context)	
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'nomina': nomina, 
				'name': nom3,
				'stage': stage,
				'tipo_nomina': tipo_nomina,
				'tipo_beca': beca,
				'nombre': nom3,
				'res_name': nom3,
				'datas': base64.encodestring(archivo3.read()),
				'datas_fname': nom3,
				'res_model': 'becados.nomina',
				}, context=context)
	
	
	#Función para la generación de reportes en XLS de la nómina	
	def generar_xls(self, cr, uid, nomina, tipo_nomina, tipo_beca, mes, data1, stage, context):
		
		if stage != 'prenomina' and stage != 'cancelado':
			#Preparación de la descripción del tipo de beca
			#~ if 'ESPECIAL' in tipo_beca:
				#~ cod_beca = '50'
				#~ beca = 'BECA ESPECIAL'
			#~ elif 'SOCIAL' in tipo_beca:
				#~ cod_beca = '10'
				#~ beca = 'BECA SOCIAL'
			#~ elif 'EXCELENCIA' in tipo_beca:
				#~ cod_beca = '02'
				#~ beca = 'BECA EXCELENCIA'
			#~ else:
				#~ cod_beca = '01'
				#~ beca = 'BECA CYBERGUÍA'
			
			beca = "GENERAL"
			
			#Generación del nombre del reporte
			#~ fecha = time.strftime('(%d-%m-%y)')
			#~ dia = time.strftime('%d')
			anyo = time.strftime('%Y')
			#~ fecha = dia+"-"+mes+"-"+anyo
			nombre_archivo = "XLS." + "RESUMEN GENERAL" + "-" + mes.upper() + "-" + anyo +'.'+ 'xls'
			
			#Proceso de consulta de todos los becados
			modelo = self.pool.get('hr.employee') #Modelo a consultar
			consulta = modelo.search(cr, uid, [('categoria','=','1')])
			leer_consulta = modelo.read(cr, uid, consulta, context=context)				
			
			#Generación del reporte (Pendiente por cargar la data)
			style0 = xlwt.easyxf('font: name Times New Roman, colour black, bold on')
			style1 = xlwt.easyxf('',num_format_str='D-M-YY')
			wb = xlwt.Workbook()
			ws = wb.add_sheet('Cierre de Nomina',cell_overwrite_ok=True)
			ws.write(0, 0, 'cedula', style0)
			ws.write(0, 1, 'apellido1', style0)
			ws.write(0, 2, 'apellido2', style0)
			ws.write(0, 3, 'nombre1', style0)
			ws.write(0, 4, 'nombre2', style0)
			ws.write(0, 5, 'asignacion', style0)
			ws.write(0, 6, 'nro_cta', style0)
			ws.write(0, 7, 'banco', style0)
			ws.write(0, 8, 'fecha_nac', style0)
			ws.write(0, 9, 'cargo', style0)
			ws.write(0, 10, 'direccion', style0)
			ws.write(0, 11, 'telefono', style0)
			ws.write(0, 12, 'estatus', style0)
			ws.write(0, 13, 'fecha_ingreso', style0)
			ws.write(0, 14, 'fecha_egreso', style0)
			ws.write(0, 15, 'cod_tipo_beca', style0)
			ws.write(0, 16, 'tipo_beca', style0)
			ws.write(0, 17, 'sede/unidad', style0)
			ws.write(0, 18, 'grado_instruc', style0)
			ws.write(0, 19, 'camisa', style0)
			ws.write(0, 20, 'pantalon', style0)
			ws.write(0, 21, 'zapato', style0)
			ws.write(0, 22, 'sexo', style0)
			ws.write(0, 23, 'edad', style0)
			i = 1
			j = 0
			for registro in leer_consulta:
				#Preparación de los campos en variables
				t_beca = registro['tipo_beca']
				sede = registro['sede']
				grado_instruc = registro['grado_instruccion']
				#~ print "TIPO_BECA: "+str(t_beca)+ "SEDE: "+str(sede)+ "GRADO: "+str(grado_instruc)
				
				cedula = registro['cedula']
				primer_apellido = registro['primer_apellido'].upper()
				if not registro['segundo_apellido']:
					segundo_apellido = ""
				else:
					segundo_apellido = registro['segundo_apellido'].upper()
				primer_nombre = registro['primer_nombre'].upper()
				if not registro['segundo_nombre']:
					segundo_nombre = ""
				else:	
					segundo_nombre = registro['segundo_nombre'].upper()
				if not registro['tipo_beca']:
					cod_beca = ""
					asignacion = ""
				else:
					model_tipo_beca = self.pool.get('becados.tipobeca')
					consulta_tipo_beca = model_tipo_beca.search(cr, uid, [('id','=',registro['tipo_beca'][0])])
					leer_tipo_beca = model_tipo_beca.read(cr, uid, consulta_tipo_beca, context=context)
					cod_beca = ""
					asignacion = ""
					for campo in leer_tipo_beca:
						cod_beca = campo['cod_t_beca']
						asignacion = campo['asignacion']
				if not registro['numero_cuenta']:
					numero_cuenta = ""
				else:
					numero_cuenta = registro['numero_cuenta']
				if not registro['entidad_bancaria']:
					entidad_bancaria = ""
				else:
					entidad_bancaria = str(registro['entidad_bancaria'][1]).upper()
				if not registro['fecha_nacimiento']:
					fecha_nacimiento = ""
				else:
					fecha_nacimiento = registro['fecha_nacimiento']
				cargo = "BECADO"
				direccion = registro['direccion'].upper()
				tlf_movil = registro['tlf_movil']
				if not registro['status']:
					status = ""
				else:
					if registro['status'] == '1':
						status = 'Activo'
					elif registro['status'] == '2':
						status = 'Periodo de gracia'
					elif registro['status'] == '3':
						status = 'Permiso de reposo'
					elif registro['status'] == '4':
						status = 'Permiso no remunerado'
					elif registro['status'] == '5':
						status = 'Suspendido'
					elif registro['status'] == '6':
						status = 'Vacaciones'
					elif registro['status'] == '7':
						status = 'Egresado'
				fecha_ingreso = registro['fecha_ingreso']
				if not registro['fecha_egreso']:
					fecha_egreso = ""
				else:
					fecha_egreso = registro['fecha_egreso']
				if not registro['tipo_beca']:
					tipo_beca_name = ""
				else:
					tipo_beca_name = t_beca[1]
				if not registro['sede']:
					desc_sede = ""
				else:
					model_sede = self.pool.get('becados.sedes')
					consulta_sede = model_sede.search(cr, uid, [('id','=',registro['sede'][0])])
					leer_sede = model_sede.read(cr, uid, consulta_sede, context=context)
					desc_sede = ""
					for campo in leer_sede:
						desc_sede = campo['descripcion']
				grado_instruccion = grado_instruc[1].upper()
				if not registro['camisa']:
					camisa = ""
				else:
					camisa = registro['camisa'].upper()
				if not registro['pantalon']:
					pantalon = ""
				else:
					pantalon = registro['pantalon']
				if not registro['zapato']:
					zapato = ""
				else:
					zapato = registro['zapato']
				if not registro['sexo']:
					sexo = ""
				else:
					sexo = registro['sexo'].upper()
				if not registro['edad']:
					edad = ""
				else: 
					edad = registro['edad']
				
				#Carga de los datos en las celdas del xls
				ws.write(i, 0, cedula)
				ws.write(i, 1, primer_apellido)
				ws.write(i, 2, segundo_apellido) #Da error si el dato es str en vez unicode, es de
				ws.write(i, 3, primer_nombre)
				ws.write(i, 4, segundo_nombre)
				ws.write(i, 5, asignacion)
				ws.write(i, 6, numero_cuenta)
				ws.write(i, 7, entidad_bancaria)
				ws.write(i, 8, fecha_nacimiento)
				ws.write(i, 9, cargo)
				ws.write(i, 10, direccion)
				ws.write(i, 11, tlf_movil)
				ws.write(i, 12, status)
				ws.write(i, 13, fecha_ingreso)
				ws.write(i, 14, fecha_egreso)
				ws.write(i, 15, cod_beca)
				ws.write(i, 16, tipo_beca_name)
				ws.write(i, 17, desc_sede)
				ws.write(i, 18, grado_instruccion)
				ws.write(i, 19, camisa)
				ws.write(i, 20, pantalon)
				ws.write(i, 21, zapato)
				ws.write(i, 22, sexo.capitalize()) #Retorna:una copia de la cadena con la primera letra en mayúsculas 
				ws.write(i, 23, edad)
				i+=1
			#~ ws.write(2, 0, 4)
			#~ ws.write(2, 1, 1)
			#~ ws.write(2, 2, xlwt.Formula("A3+B3"))
			
			#Guardar reporte en una ruta específica
			#Ruta local
			#~ wb.save('openerp/addons/desarrollo_social/reportes/nominas/'+nombre_archivo)
			#Ruta en el servidor
			wb.save('/home/administrador/openerp70/modules/desarrollo_social/reportes/nominas/'+nombre_archivo)
			
			#Abrir el archivo del reporte para poder registrarlo
			#Ruta local
			#~ archivo = open('openerp/addons/desarrollo_social/reportes/nominas/'+nombre_archivo)
			#Ruta en el servidor
			archivo = open('/home/administrador/openerp70/modules/desarrollo_social/reportes/nominas/'+nombre_archivo)
			
			#Registro del archivo de reporte en la base de datos
			id_att = self.pool.get('ir.attachment').create(cr, uid, {
				'nomina': nomina, 
				'name': nombre_archivo,
				'stage': stage,
				'tipo_nomina': tipo_nomina,
				'tipo_beca': beca,
				'nombre': nombre_archivo,
				'res_name': nombre_archivo,
				'datas': base64.encodestring(archivo.read()),
				'datas_fname': nombre_archivo,
				'res_model': 'becados.nomina',
				}, context=context)
			
			
	def carga_beca(self, cr, uid, ids, tipo_beca, context=None):
		valores = {}
		
		modelo = self.pool.get("becados.tipobeca")
		id_modelo = modelo.browse(cr, uid, tipo_beca, context=context)
		
		beca_general = ""
		beca_especifica = id_modelo.tipo_beca
		
		if 'ESPECIAL' in beca_especifica:
			beca_general = 'BECA ESPECIAL'
		elif 'SOCIAL' in beca_especifica:
			beca_general = 'BECA SOCIAL'
		elif 'EXCELENCIA' in beca_especifica:
			beca_general = 'BECA EXCELENCIA'
		else:
			beca_general = 'BECA CYBERGUÍA'
		
		valores.update({'beca' : beca_general,})
		
		return {'value': valores}
		
	#Función para eliminar los acentos de cualquier cadena		
	def elimina_tildes(self, s):
		"""
		Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
		"""
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
		
	def format_fecha(self, fecha):
		date = fecha.split("-")
		nueva_fecha = date[2]+"-"+date[1]+"-"+date[0]
		return nueva_fecha
	
	#Función que fija el mes de la nómina según la fecha actual
	def _fijar_mes(self, cr, uid, ids, context=None): # Pendiente por implementar
		values = {}
		fecha = date.today() #Fecha actual
		meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
		i = 1
		for mes in meses:
			if i == int(fecha.month):
				values.update({'mes' : mes,})
			i = i + 1
			
		return {'value' : values}
  	
  	
	#Definición de las columnas del modelo----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	_columns = {
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
		'tipo_nomina' : fields.many2one('becados.tiponomina','Tipo de Nómina',required=True),
		'tipo_beca' : fields.many2one("becados.tipobeca","Tipo de Beca",required=True),
		'beca' : fields.char(string="Beca",required=False),
		'banco' : fields.many2one("becados.bancos", "Banco", required = False), 
		#~ 'ejes' : fields.many2one("becados.ejes","Eje",required=False),
		#~ 'sedes' : fields.many2one("becados.sedes","Sede",required=False),
		'becados' : fields.many2many("hr.employee", "proceso_nomina", "becados_nomina_id", "hr_employee_id", "Becados", required=True),
		'nomina_individual' : fields.one2many("becados.nominaindividual", "nomina", string="Nóminas", required=False),
		'archivos' : fields.one2many("ir.attachment", "nomina", string="Archivos de nómina", required="False"),
		#Podemos ver que el campo de 'becados', de tipo many2many, contiene 5 parametros:
		#"hr.employee", indica el nombre del modelo al que se va a hacer relación (modelo de empleados).
		#"proceso_nomina", indica el nombre del modelo que se creará para ser intermediario entre el modelo actual (modelo de nomina) y el modelo a relacionar (modelo de empleados).
		#"becados_nomina_id", indica un nombre de id que representará al modelo actual (modelo de nomina) en el modelo intermediario.
		#"hr_employee_id", indica un nombre de id que representará al modelo a relacionar (modelo de empleados) en el modelo intermediario.
		'stage_id' : fields.selection((('prenomina','Pre-nómina'),('nomina','Nómina'),('cierre','Cerrado'),('cancelado','Cancelado')), "Estado", required=True),
		'inicio_periodo' : fields.date("Desde",required=True),
		'fin_periodo' : fields.date("Hasta",required=True),
	}
	
	_defaults = {
		'stage_id' : 'prenomina',
		'anyo' : lambda *a: time.strftime("%Y"),
		'inicio_periodo' : lambda *a: time.strftime('%Y-%m-01'), # Fecha desde
		'fin_periodo' : lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10], # Fecha hasta
		#~ 'mes' : _fijar_mes, 
		#~ 'tipo_nomina' : '1'
		#~ 'status' : '1',
	}
