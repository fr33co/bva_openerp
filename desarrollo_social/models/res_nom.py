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
		

def gen_res_nom(cr,nomina,periodo_ini,periodo_fin,tipo_beca,mes,data):
	#Variables globales
	monto_total = 0
	
	# Instancia de la clase heredada L es horizontal y P es vertical
	pdf=clases_reportes.PDF2(orientation='P',unit='mm',format='A4') #HORIENTACION DE LA PAGINA

	#pdf.set_title(title)
	pdf.set_author('José Solorzano')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	pdf.set_font('Arial','B',10) # CARACTERÍSTICAS DE LA FUENTE
	pdf.set_fill_color(255,255,255) # COLOR DE BORDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	pdf.set_margins(8,10,10) # MARGEN DEL DOCUMENTO

	pdf.ln(10) # Saldo de linea
	# 10 y 50 eje x y y 200 dimencion

	pdf.ln(1)
	pdf.set_x(45)
	pdf.cell(130,6,"PERIODO DE LA NÓMINA DEL ".decode("UTF-8")+periodo_ini+" AL "+periodo_fin,'LTRB',0,'C',1)
	pdf.ln(10)
	pdf.cell(17,6,"",'LTB',0,'C',1)
	pdf.cell(45,6,"NÓMINAS".decode("UTF-8"),'TB',0,'L',1)
	pdf.cell(78,6,"Cant. de Persona(s)",'TB',0,'R',1)
	pdf.cell(50,6,"Monto",'TBR',1,'C',1)
	
	#Cosultamos los bancos existentes en base de datos
	modelo_bancos = "becados_bancos"
	cr.execute('SELECT id, banco, descripcion FROM '+modelo_bancos+' ORDER BY banco')
	i = 0
	for bancos in cr.fetchall():
		
		monto_sub_total = 0
		
		if bancos[1].upper() == "VENEZUELA": #Tomamos en cuenta sólo los registros del banco 'VENEZUELA'
		
			j = 0 #Contador para registros
			for registro in data:
				#Verificamos que el banco del registro sea 'VENEZUELA' 
				if registro[7] == "VENEZUELA":
					#Para el cálculo del monto por banco tomamos en cuenta el valor del registro en la posición correspondiente al monto
					if registro[5] == "" or registro[5] == 0.00:
						reg_m = float(0.00)
					else:
						reg_m = float(registro[5])
					#~ print "Monto"+str(j+1)+": "+str(reg_m)
					#SUBTOTAL
					monto_sub_total = monto_sub_total + reg_m
					
					j = j +1 #Incremento del contador de registros
			
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
			
			pdf.cell(10,6,"",'',0,'C',1)
			pdf.cell(70,6,"BANCO: "+bancos[1].upper(),'',0,'L',1)
			pdf.cell(55,6,"",'',0,'C',1)
			pdf.cell(55,6,"",'',1,'C',1)

			pdf.set_font('Arial','',10) # CARACTERÍSTICAS DE LA FUENTE
			pdf.cell(10,6,"1",'B',0,'C',1)
			pdf.cell(70,6,beca.decode("UTF-8"),'B',0,'L',1)
			pdf.cell(55,6,str(j),'B',0,'R',1)
			pdf.cell(55,6,str(monto_sub_total),'B',1,'C',1)

			pdf.set_font('Arial','B',10) # CARACTERÍSTICAS DE LA FUENTE
			pdf.cell(10,6,"",'B',0,'C',1)
			pdf.cell(70,6,"TOTAL "+bancos[1].upper(),'B',0,'R',1)
			pdf.cell(55,6,str(j),'B',0,'R',1)
			pdf.cell(55,6,str(monto_sub_total),'B',1,'C',1)
			pdf.ln(1)
			
			i = i + 1
		
		monto_total = monto_total + monto_sub_total
		
	pdf.cell(10,6,"",'LTB',0,'C',1)
	pdf.cell(70,6,"TOTAL GENERAL NÓMINA(S)".decode("UTF-8"),'TB',0,'L',1)
	pdf.cell(55,6,str(j),'TB',0,'R',1)
	pdf.cell(55,6,str(monto_total),'TBR',1,'C',1)

	#~ pdf.line(10, 40, 200, 40, "dash") PROBAR PARA GENERAR LÍNEA PUNTEADA
	
	
	#Generación del nombre del reporte
	#~ fecha = time.strftime('(%d-%m-%y)')
	#~ dia = time.strftime('%d')
	anyo = time.strftime('%Y')
	#~ fecha = dia+"-"+mes+"-"+anyo
	nombre_archivo = 'RESUMEN_NOMINA_'+elimina_tildes(beca.decode("UTF-8").upper()) + "-" + mes.upper() + "-" + anyo +'.'+ 'pdf'
	
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
