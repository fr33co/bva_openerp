# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import clases_reportes
import unicodedata

#Función para eliminar los acentos de cualquier cadena		
def elimina_tildes(s):
		"""
		Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
		"""
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
		

def gen_res_bank(cr, uid, id_nomina, nomina, periodo_ini, periodo_fin, tipo_beca, mes, data, stage, context):
	#Variables globales
	monto_total = 0
	activos = 0
	suspendidos = 0
	
	#Instancia de la clase heredada L es horizontal y P es vertical
	pdf=clases_reportes.PDF(orientation='P',unit='mm',format='A4') #HORIENTACION DE LA PAGINA

	#pdf.set_title(title)
	pdf.set_author('José Solorzano')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	pdf.set_font('Times','',12) # TAMANO DE LA FUENTE
	pdf.set_fill_color(255,255,255) # COLOR DE BORDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	pdf.set_margins(8,10,10) # MARGEN DEL DOCUMENTO

	pdf.ln(50) # Saldo de linea
	# 10 y 50 eje x y y 200 dimencion

	pdf.set_y(25)
	pdf.set_x(10)
	pdf.set_font('Times','',8)
	pdf.write(10,"TIPO NÓMINA ".decode("UTF-8")+nomina.upper())
	pdf.ln(2)
	pdf.set_y(30)
	pdf.set_x(10)
	pdf.set_font('Times','',8)
	pdf.write(10,"PERÍODO DEL ".decode("UTF-8")+periodo_ini+" AL "+periodo_fin)
	#~ pdf.line(10, 40, 200, 40)
	
	#Cosultamos los bancos existentes en base de datos
	modelo_bancos = "becados_bancos"
	cr.execute('SELECT id, banco, descripcion FROM '+modelo_bancos+' ORDER BY banco')
	i = 0 #Contador para bancos
	for bancos in cr.fetchall():
		
		monto_sub_total = 0
		
		if bancos[1].upper() == "VENEZUELA": #Tomamos en cuenta sólo los registros del banco 'VENEZUELA'
			b_social = 0
			b_esp_comision = 0
			b_esp_cyber = 0
			b_cyber = 0
			j = 0 #Contador para registros
			for registro in data:
				#Contamos los becados activos e inactivos
				if registro[12] == '1':
					activos = int(activos) + 1
				if registro[12] == '5':
					suspendidos = int(suspendidos) + 1
					
				#Verificamos que el banco del registro sea 'VENEZUELA' 
				if registro[7] == "VENEZUELA":
					#Para el cálculo del monto por banco tomamos en cuenta el valor del registro en la posición correspondiente
					if registro[5] == "" or registro[5] == 0.00:
						reg_m = float(0.00)
					else:
						reg_m = float(registro[5])
					#~ print "Monto"+str(j+1)+": "+str(reg_m)
					#Cantidad por beca social
					if registro[17] == "004":
						b_social = b_social + reg_m
					#Cantidad por beca especial comisión de beca
					if registro[17] == "005":
						b_esp_comision = b_esp_comision + reg_m
					#Cantidad por beca especial cyberguía
					if registro[17] == "006":
						b_esp_cyber = b_esp_cyber + reg_m
					#Cantidad por beca cyberguía
					if registro[17] == "007":
						b_cyber = b_cyber + reg_m
						
					#SUBTOTAL
					monto_sub_total = monto_sub_total + reg_m 
					
					j = j +1 #Incremento del contador de registros
			
			#~ print "\nMonto beca social: "+str(b_social)		
			#~ print "Monto beca especial comision de beca: "+str(b_esp_comision)		
			#~ print "Monto beca especial cyberguia: "+str(b_esp_cyber)		
			#~ print "Monto beca cyberguia: "+str(b_cyber)		
			#~ print "Monto total: "+str(monto_sub_total)		
			#~ print "Becados activos: "+str(activos)+", suspendidos: "+str(suspendidos)
			
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
			
			pdf.ln(10)
			pdf.set_x(75)
			pdf.cell(70,6,"NÓMINA DEL PERSONAL BANCO ".decode("UTF-8")+bancos[1].upper(),'',0,'C',1)
			pdf.ln(10)
			pdf.set_text_color(77,77,77)
			pdf.cell(20,6,"CÓDIGO".decode("UTF-8"),'LTB',0,'C',1)
			pdf.cell(80,6,"CONCEPTOS",'TB',0,'C',1)
			pdf.cell(30,6,"ASIGNACIONES",'TB',0,'C',1)
			pdf.cell(30,6,"DEDUCCIONES",'TB',0,'C',1)
			pdf.cell(30,6,"NETO A PAGAR",'TBR',1,'C',1)

			pdf.set_text_color(0,0,0)
			pdf.cell(20,6,cod_beca,'B',0,'C',1)
			pdf.cell(80,6,beca.decode("UTF-8"),'B',0,'C',1)
			pdf.cell(30,6,"",'B',0,'C',1)
			pdf.cell(30,6,"",'B',0,'C',1)
			pdf.cell(30,6,"",'B',1,'C',1)
			
			#Verificamos el monto para cada tipo de beca y si es superior a cero imprimimos la fila con sus celdas y datos
			if b_social > 0:
				pdf.set_text_color(77,77,77)
				pdf.cell(20,6,'004','B',0,'C',1)
				pdf.cell(80,6,'BECA SOCIAL','B',0,'C',1)
				pdf.cell(30,6,str(b_social),'B',0,'C',1)
				pdf.cell(30,6,"",'B',0,'C',1)
				pdf.cell(30,6,"",'B',1,'C',1)
			if b_esp_comision > 0:
				pdf.set_text_color(77,77,77)
				pdf.cell(20,6,'005','B',0,'C',1)
				pdf.cell(80,6,'BECA ESPECIAL (COMISIÓN BECA)'.decode("UTF-8"),'B',0,'C',1)
				pdf.cell(30,6,str(b_esp_comision),'B',0,'C',1)
				pdf.cell(30,6,"",'B',0,'C',1)
				pdf.cell(30,6,"",'B',1,'C',1)
			if b_esp_cyber > 0:
				pdf.set_text_color(77,77,77)
				pdf.cell(20,6,'006','B',0,'C',1)
				pdf.cell(80,6,'BECA ESPECIAL (CYBERGUÍA)'.decode("UTF-8"),'B',0,'C',1)
				pdf.cell(30,6,str(b_esp_cyber),'B',0,'C',1)
				pdf.cell(30,6,"",'B',0,'C',1)
				pdf.cell(30,6,"",'B',1,'C',1)
			if b_cyber > 0:
				pdf.set_text_color(77,77,77)
				pdf.cell(20,6,'007','B',0,'C',1)
				pdf.cell(80,6,'BECA CYBERGUÍA'.decode("UTF-8"),'B',0,'C',1)
				pdf.cell(30,6,str(b_cyber),'B',0,'C',1)
				pdf.cell(30,6,"",'B',0,'C',1)
				pdf.cell(30,6,"",'B',1,'C',1)
			pdf.set_text_color(0,0,0)
			pdf.cell(20,6,cod_beca,'B',0,'C',1)
			pdf.cell(80,6,beca.decode("UTF-8"),'B',0,'C',1)
			pdf.cell(30,6,str(monto_sub_total),'B',0,'C',1)
			pdf.cell(30,6,"",'B',0,'C',1)
			pdf.cell(30,6,str(monto_sub_total),'B',1,'C',1)

			pdf.cell(20,6,"",'B',0,'C',1)
			pdf.cell(80,6,"TOTAL NÓMINA DEL PERSONAL BANCO VENEZUELA".decode("UTF-8"),'B',0,'C',1)
			pdf.cell(30,6,str(monto_sub_total),'B',0,'C',1)
			pdf.cell(30,6,"",'B',0,'C',1)
			pdf.cell(30,6,str(monto_sub_total),'B',1,'C',1)
			pdf.ln(1)
		
		monto_total = monto_total + monto_sub_total

	pdf.cell(20,6,"",'LT',0,'C',1)
	pdf.cell(80,6,"TOTAL GENERAL NÓMINA:".decode("UTF-8"),'T',0,'C',1)
	pdf.cell(30,6,str(monto_total),'T',0,'C',1)
	pdf.cell(30,6,"",'T',0,'C',1)
	pdf.cell(30,6,str(monto_total),'TR',1,'C',1)

	pdf.cell(80,6,"CANT. PERSONAS ACTIVA:",'L',0,'R',1)
	pdf.cell(20,6,str(activos),'',0,'C',1)
	pdf.cell(30,6,"",'',0,'C',1)
	pdf.cell(30,6,"",'',0,'C',1)
	pdf.cell(30,6,"",'R',1,'C',1)

	pdf.cell(80,6,"CANT. PERSONAS SUSPENDIDAS:",'LB',0,'R',1)
	pdf.cell(20,6,str(suspendidos),'B',0,'C',1)
	pdf.cell(30,6,"",'B',0,'C',1)
	pdf.cell(30,6,"",'B',0,'C',1)
	pdf.cell(30,6,"",'BR',1,'C',1)
	
	i = i + 1 #Incremento del contador de bancos
	
	#Generación del nombre del reporte
	#~ fecha = time.strftime('(%d-%m-%y)')
	#~ dia = time.strftime('%d')
	anyo = time.strftime('%Y')
	#~ fecha = dia+"-"+mes+"-"+anyo
	nombre_archivo = 'RESUMEN_CONCEPTOS_'+elimina_tildes(beca.decode("UTF-8").upper()) + "-" + mes.upper() + "-" + anyo +'.'+ 'pdf'
	
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
