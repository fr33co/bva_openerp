# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import clases_reportes
import unicodedata

#Función para formartear fechas de 'YY-MM-DD' a 'DD-MM-YY'
def format_fecha(fecha):
		date = fecha.split("-")
		nueva_fecha = date[2]+"-"+date[1]+"-"+date[0]
		return nueva_fecha

#Función para eliminar los acentos de cualquier cadena		
def elimina_tildes(s):
		"""
		Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
		"""
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
		

#Función para generar el reporte de nómina detallado por banco
def gen_detallado(cr, uid, id_nomina, nomina, periodo_ini, periodo_fin, tipo_beca, mes, data, stage, context):
	#Variables globales
	monto_total = 0
	activos = 0
	suspendidos = 0
	
	#Contamos los becados activos e inactivos
	for registro in data:
		if registro[12] == '1':
			activos = int(activos) + 1
		if registro[12] == '5':
			suspendidos = int(suspendidos) + 1
						
	# Instancia de la clase heredada L es horizontal y P es vertical
	pdf=clases_reportes.PDF3(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PÁGINA

	#pdf.set_title(title)
	pdf.set_author('José Solorzano')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	pdf.set_font('Times','',12) # TAMAÑO DE LA FUENTE
	pdf.set_fill_color(255,255,255) # COLOR DE BORDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	pdf.set_margins(8,10,10) # MARGEN DEL DOCUMENTO

	pdf.ln(50) # Saldo de linea
	# 10 y 50 eje x y y 200 dimensión
	
	#Modelos a utilizar
	modelo_becados = "hr_employee"
	modelo_bancos = "becados_bancos"
	modelo_sedes = "becados_sedes"
	modelo_nominaindividual = "becados_nominaindividual"
	modelo_tipobecas = "becados_tipobeca"
	
	#Preparación del código y descripción del tipo de beca
	if 'ESPECIAL' in tipo_beca:
		cod_beca = '50'
		beca = 'BECA ESPECIAL'
	elif 'SOCIAL' in tipo_beca:
		cod_beca = '10'
		beca = 'BECA SOCIAL'
	elif 'EXCELENCIA' in tipo_beca:
		cod_beca = '02'
		beca = 'BECA EXCELENCIA'
	else:
		cod_beca = '01'
		beca = 'BECA CYBERGUÍA'
		
	
	#Cosultamos los bancos
	cr.execute('SELECT id, banco, descripcion FROM '+modelo_bancos+' ORDER BY banco')
	i = 0 #Contador para paginar por banco 
	j = 0 #Contador para el número de becados totales
	g = 0
	subtotal_banco = 0 #Acumulador para el monto subtotal por banco
	for bancos in cr.fetchall():
		#Inicialización en cero del acumulador del subtotal por sede cada vez que inicia el ciclo
		subtotal_banco = 0
		
		#verificamos si existen becados para cada banco
		becados_por_banco = "SELECT count(*) AS num_becados FROM "+modelo_nominaindividual+" AS nom_i INNER JOIN "+modelo_becados+" AS he ON nom_i.becado=he.id WHERE nom_i.nomina="+str(id_nomina)+" AND he.entidad_bancaria="+str(bancos[0])
		cr.execute(becados_por_banco)
		for num_b_b in cr.fetchall():
			numero_becados_banc = num_b_b[0] #Número de becados para la sede de la iteración actual
		#~ print "Becados del banco "+str(bancos[1])+": "+str(numero_becados_banc)
		
		#Si efectivamente existe becados para el banco actual se procede a listarlos por sede
		if numero_becados_banc > 0:
		 
			#Apertura del grupo del banco
			desc_banco = bancos[1].upper()
			#CABECERA DE BANCO
			pdf.set_y(25)
			pdf.set_x(10)
			pdf.set_font('Arial','',10)
			pdf.write(10,"TIPO NÓMINA ".decode("UTF-8")+nomina.upper())
			pdf.ln(2)
			pdf.set_y(30)
			pdf.set_x(10)
			pdf.set_font('Arial','',10)
			pdf.write(10,"PERÍODO DEL ".decode("UTF-8")+periodo_ini+" AL "+periodo_fin)
			#~ pdf.line(10, 40, 200, 40)
			
			pdf.ln(10)
			pdf.set_x(75)
			pdf.cell(70,6,"NÓMINA DEL PERSONAL BANCO ".decode("UTF-8")+desc_banco,'',0,'C',1)
			pdf.ln(5)
			pdf.set_text_color(77,77,77)
			pdf.set_font('Arial','',8)
			pdf.cell(15,6,"FPE",'LTB',0,'C',1)
			pdf.cell(15,6,"DÍAS".decode("UTF-8"),'TB',0,'C',1)
			pdf.cell(20,6,"CÓDIGO".decode("UTF-8"),'TB',0,'C',1)
			pdf.cell(53,6,"CONCEPTOS",'TB',0,'C',1)
			pdf.cell(30,6,"ASIGNACIONES",'TB',0,'C',1)
			pdf.cell(30,6,"DEDUCCIONES",'TB',0,'C',1)
			pdf.cell(30,6,"NETO A COBRAR",'TBR',1,'C',1)
			
			pdf.set_font('Arial','',10)
			pdf.set_text_color(0,0,0)
			pdf.cell(20,6,cod_beca,'B',0,'L',1)
			pdf.cell(68,6,beca.decode("UTF-8"),'B',0,'L',1)
			pdf.cell(105,6,"",'B',1,'C',1)
			
			#~ Seleccionamos las sedes según los bancos 
			consulta2 = 'SELECT s.id, s.sede, s.descripcion, s.codigo FROM '+modelo_sedes+' AS s GROUP BY s.sede, s.descripcion, s.id'
			#~ print consulta2
			cr.execute(consulta2)
			subtotal_sede = 0 #Preparación de un acumulador para el monto subtotal por sede
			for sede in cr.fetchall():
				#Validamos el código de la sede
				if not sede[3]:
					cod_sede = ""
				else:
					cod_sede = sede[3]		
				#Inicialización en cero del acumulador del subtotal por sede cada vez que inicia el ciclo
				subtotal_sede = 0
				
				#verificamos si existen becados para cada sede
				becados_por_sedes = "SELECT count(*) AS num_becados FROM "+modelo_nominaindividual+" AS nom_i INNER JOIN "+modelo_becados+" AS he ON nom_i.becado=he.id WHERE nom_i.nomina="+str(id_nomina)+" AND he.entidad_bancaria="+str(bancos[0])+" AND he.sede="+str(sede[0])
				cr.execute(becados_por_sedes)
				for num_b in cr.fetchall():
					numero_becados = num_b[0] 
				#~ print "CANTIDAD DE BECADOS PARA LA SEDE "+sede[1].encode("UTF-8").decode("UTF-8").upper()+": "+str(numero_becados)
				
				if numero_becados > 0:
					#CABECERA DE SEDE
					#Apertura del grupo de la sede
					pdf.set_font('Arial','',7)
					pdf.set_text_color(77,77,77)
					pdf.cell(20,6,cod_sede,'B',0,'L',1)
					pdf.cell(68,6,sede[2],'B',0,'R',1)
					pdf.cell(105,6,"",'B',1,'C',1)
					
					#~ Listamos los becados suspendidos según la nómina, el banco y la sede
					consulta3 = "SELECT he.cedula, he.status, he.primer_apellido, he.segundo_apellido, he.primer_nombre, he.segundo_nombre, tb.tipo_beca, tb.asignacion, he.numero_cuenta, he.fecha_ingreso, nom_i.monto, he.sede, tb.cod_t_beca FROM "+modelo_nominaindividual+" AS nom_i INNER JOIN "+modelo_becados+" AS he ON nom_i.becado=he.id INNER JOIN "+modelo_tipobecas+" AS tb ON he.tipo_beca=tb.id WHERE nom_i.nomina="+str(id_nomina)+" AND he.entidad_bancaria="+str(bancos[0])+" AND he.sede="+str(sede[0])+" ORDER BY he.status"
					#~ print consulta3
					cr.execute(consulta3)
					k = 0 #Contador para el número de becados por sede
					for becado in cr.fetchall():						
						#~ Validar campos que puedan venir vacíos
						if not becado[0]:
							cedula = ""
						else:
							cedula = becado[0]
						#------------------------------------------
						if not becado[1]:
							status = ""
						else:
							if str(becado[1]) == "5":
								status = "***Suspendido***"
							else:
								status = ""
						#------------------------------------------
						if not becado[2]:
							p_ape = ""
						else:
							p_ape = becado[2].encode("UTF-8").decode("UTF-8").upper()
						#------------------------------------------
						if not becado[3]:
							s_ape = ""
						else:
							s_ape = becado[3][0].upper()
						#------------------------------------------
						if not becado[4]:
							p_nom = ""
						else:
							p_nom = becado[4].encode("UTF-8").decode("UTF-8").upper()
						#------------------------------------------
						if not becado[5]:
							s_nom = ""
						else:
							s_nom = becado[5][0].upper()
						#------------------------------------------
						if not becado[6]:
							tb = ""
						else:
							tb = becado[6].encode("UTF-8").decode("UTF-8")
						#------------------------------------------
						if not becado[7]:
							asig = ""
						else:
							asig = str(float(int(becado[7])))
						#------------------------------------------
						if not becado[8]:
							n_cuenta = ""
						else:
							n_cuenta = becado[8]
						#------------------------------------------
						if not becado[9]:
							f_ingreso = ""
						else:
							f_ingreso = becado[9]
						#------------------------------------------
						if not becado[10]:
							monto = 0
						else:
							monto = becado[10]
						#------------------------------------------
						if not sede[2]:
							sd = ""
						else:
							sd = sede[2]
						#------------------------------------------
						if not becado[12]:
							cod_t_beca = ""
						else:
							cod_t_beca = becado[12]
						
						pdf.ln(1)
						pdf.set_text_color(0,0,0)
						pdf.cell(17,5,cedula,'T',0,'L',1)
						pdf.cell(45,5,p_ape+" "+s_ape+" "+p_nom+" "+s_nom,'T',0,'C',1)
						pdf.cell(53,5,tb,'T',0,'L',1)
						pdf.cell(19,5,"",'T',0,'C',1)
						pdf.cell(40,5,"CTA:"+n_cuenta,'T',0,'C',1)
						pdf.cell(19,5,"",'T',1,'C',1)

						pdf.set_text_color(77,77,77)
						pdf.cell(25,5,"",'',0,'L',1)
						pdf.set_text_color(0,0,0)
						pdf.cell(37,5,"",'',0,'C',1)
						pdf.cell(30,5,"INGRESO M.:",'',0,'L',1)
						pdf.cell(42,5,"%.2f" % round(float(asig),2),'',0,'L',1)
						pdf.cell(30,5,"FEC. ING.: "+format_fecha(f_ingreso),'',0,'C',1)
						pdf.cell(29,5,"",'',1,'C',1)
						
						pdf.set_font('Arial','',8)
						pdf.cell(193,3,"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ __ _ _ _ _ _ __ _ _ _ _ _ _",'',1,'C',1)
						
						pdf.set_font('Arial','',7)
						pdf.cell(25,5,status,'',0,'L',1)
						pdf.cell(35,5,str(cod_t_beca)+"   ",'',0,'R',1)
						pdf.cell(44,5,tb,'',0,'L',1)
						pdf.cell(30,5,"%.2f" % round(monto,2),'',0,'R',1)
						pdf.cell(30,5,"",'',0,'C',1)
						pdf.cell(29,5,"",'',1,'R',1)
						
						pdf.set_font('Arial','',8)
						pdf.cell(25,5,"",'',0,'L',1)
						pdf.cell(37,5,"",'',0,'C',1)
						pdf.cell(30,5,"",'',0,'L',1)
						pdf.cell(42,5,"-------------",'',0,'R',1)
						pdf.cell(30,5,"-------------",'',0,'L',1)
						pdf.cell(29,5,"Neto a Cobrar",'',1,'R',1)
						
						pdf.cell(52,5,"",'',0,'L',1)
						pdf.cell(10,5,"__________________________________",'',0,'C',1)
						pdf.cell(30,5,"",'',0,'L',1)
						pdf.cell(42,5,"%.2f" % round(monto,2),'',0,'R',1)
						pdf.cell(30,5,"",'',0,'C',1)
						pdf.cell(29,5,"%.2f" % round(monto,2),'',1,'R',1)

						#~ pdf.line(10, 40, 200, 40)
						pdf.cell(35,5,"",'',0,'C',1)
						pdf.cell(35,5,"FIRMA BECADO     ",'',1,'L',1)
						
						#Cálculo del subtotal por sede
						subtotal_sede = subtotal_sede + monto
						
						#Contador de becados por sede
						k = k + 1
						
						#~ print "K: "+str(k)
						#Si el contador de becados por sede iguala el número de becados registrados para la misma, imprimo el pie de la sede
						if k == numero_becados: 
							#Cierre del grupo de la sede	
							pdf.cell(25,6,"",'TB',0,'C',1)
							pdf.cell(68,6,sede[2],'TB',0,'L',1)
							pdf.cell(90,6,"",'TB',0,'C',1)
							pdf.cell(10,6,"%.2f" % round(subtotal_sede,2),'TB',1,'R',1)
							
						#Contador de becados generales
						g +=  1
						
						#Add nueva página por límite de registros
						if g == 4:
							pdf.add_page()
							#CABECERA DE BANCO
							pdf.set_y(25)
							pdf.set_x(10)
							pdf.set_font('Arial','',10)
							pdf.write(10,"TIPO NÓMINA ".decode("UTF-8")+nomina.upper())
							pdf.ln(2)
							pdf.set_y(30)
							pdf.set_x(10)
							pdf.set_font('Arial','',10)
							pdf.write(10,"PERÍODO DEL ".decode("UTF-8")+periodo_ini+" AL "+periodo_fin)
							#~ pdf.line(10, 40, 200, 40)
							
							pdf.ln(10)
							pdf.set_x(75)
							pdf.cell(70,6,"NÓMINA DEL PERSONAL BANCO ".decode("UTF-8")+desc_banco,'',0,'C',1)
							pdf.ln(5)
							pdf.set_text_color(77,77,77)
							pdf.set_font('Arial','',8)
							pdf.cell(15,6,"FPE",'LTB',0,'C',1)
							pdf.cell(15,6,"DÍAS".decode("UTF-8"),'TB',0,'C',1)
							pdf.cell(20,6,"CÓDIGO".decode("UTF-8"),'TB',0,'C',1)
							pdf.cell(53,6,"CONCEPTOS",'TB',0,'C',1)
							pdf.cell(30,6,"ASIGNACIONES",'TB',0,'C',1)
							pdf.cell(30,6,"DEDUCCIONES",'TB',0,'C',1)
							pdf.cell(30,6,"NETO A COBRAR",'TBR',1,'C',1)

							pdf.set_text_color(0,0,0)
							pdf.cell(20,6,cod_beca,'B',0,'L',1)
							pdf.cell(68,6,beca.decode("UTF-8"),'B',0,'L',1)
							pdf.cell(105,6,"",'B',1,'C',1)
							
							if k < numero_becados:
								#CABECERA DE SEDE
								pdf.set_font('Arial','',8)
								pdf.set_text_color(77,77,77)
								pdf.cell(20,6,"10-100-150",'B',0,'L',1)
								pdf.cell(68,6,sede[2],'B',0,'R',1)
								pdf.cell(105,6,"",'B',1,'C',1)
							
							#Reiniciamos el contador de becados
							g = 0
					
					
					
					#Calculo del subtotal por banco
					subtotal_banco = subtotal_banco + subtotal_sede
					
					#Calculo del total general
					monto_total = int(subtotal_banco) #monto_total = monto_total + subtotal_banco
			
					#Contador de sedes
					j = j + 1
				
			#Cierre del grupo del banco
			pdf.set_font('Arial','',10)	
			pdf.cell(15,6,cod_beca,'B',0,'L',1)
			pdf.cell(68,6,beca.decode("UTF-8"),'B',0,'L',1)
			pdf.cell(100,6,"",'B',0,'C',1)
			pdf.cell(10,6,"%.2f" % round(subtotal_banco,2),'B',1,'R',1)

			pdf.cell(20,6,"",'B',0,'L',1)
			pdf.cell(98,6,"TOTAL NÓMINA DEL PERSONAL BANCO ".decode("UTF-8")+desc_banco,'B',0,'L',1)
			pdf.cell(65,6,"",'B',0,'C',1)
			pdf.cell(10,6,"%.2f" % round(subtotal_banco,2),'B',1,'R',1)
			
			#Add nueva página por banco				
			if i % 2 == 0:
				#Nueva página
				pdf.add_page()
				#Reiniciamos el contador de becados
				g = 0
				
			i = i + 1
		
	#PIE DE TOTALES
	pdf.ln(1)
	pdf.cell(10,6,"",'LT',0,'L',1)
	pdf.cell(113,6,"TOTAL GENERAL NÓMINA:".decode("UTF-8")+"          ",'T',0,'C',1)
	pdf.cell(60,6,"%.2f" % round(monto_total,2)+"         ",'T',0,'L',1)
	pdf.cell(10,6,"%.2f" % round(monto_total,2)+"      ",'TR',1,'C',1)
	
	pdf.cell(10,6,"",'L',0,'L',1)
	pdf.cell(83,6,"          CANT. PERSONAS ACTIVA:",'',0,'C',1)
	pdf.cell(90,6,str(activos),'',0,'L',1)
	pdf.cell(10,6,"",'R',1,'L',1)
	
	pdf.cell(10,6,"",'LB',0,'L',1)
	pdf.cell(83,6,"          CANT. PERSONAS SUSPENDIDAS:",'B',0,'C',1)
	pdf.cell(90,6,str(suspendidos),'B',0,'L',1)
	pdf.cell(10,6,"",'BR',1,'L',1)
		
	#~ print "Total de bancos: "+str(i)
	#~ print "Total de sedes: "+str(j)

	#Generación del nombre del reporte
	#~ fecha = time.strftime('(%d-%m-%y)')
	#~ dia = time.strftime('%d')
	anyo = time.strftime('%Y')
	#~ fecha = dia+"-"+mes+"-"+anyo
	nombre_archivo = 'NOMINA_DETALLADO_'+elimina_tildes(beca.decode("UTF-8").upper()) + "-" + mes.upper() + "-" + anyo +'.'+ 'pdf'
	
	#Guardar reporte en una ruta específica
	#ruta local
	#~ pdf.output('openerp/addons/desarrollo_social/reportes/nominas/'+nombre_archivo,'F')
	#ruta en el servidor
	pdf.output('/home/administrador/openerp70/modules/desarrollo_social/reportes/nominas/'+nombre_archivo,'F')
	
	#Abrir el archivo del reporte para poder registrarlo
	#ruta local
	#~ archivo = open('openerp/addons/desarrollo_social/reportes/nominas/'+nombre_archivo)
	#ruta en el servidor
	archivo = open('/home/administrador/openerp70/modules/desarrollo_social/reportes/nominas/'+nombre_archivo)
		
	return nombre_archivo, archivo
	
