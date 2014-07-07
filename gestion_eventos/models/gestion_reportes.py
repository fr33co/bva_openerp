# -*- coding: utf-8 -*-
import urllib2, urllib
import time
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval
#####################################################
#from fpdf import FPDF # Importar la libreria pdf
#import fpdf # Importar la libreria pdf
####################################################
from openerp.osv import fields, osv
import base64 #Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import xlwt
import netsvc
import tools
import logging
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import commands
import math
import pdf_class # Se importa la Clase constructora del Documento PDF

from openerp.osv import osv, fields

class Gestion_reportes(osv.osv):
	_name="gestion.reportes"

	_order = 'cantidad'
	
	_rec_name = 'cantidad'

	def search_fec(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('gestion.eventos')
		
		#======================== Busqueda por código ============================

		search_ini = obj_dp.search(cr, uid, [('fecha_inicio','=',argument_search)])

		fecha_ini  = obj_dp.read(cr,uid,search_ini,context=context)

		search_fin = obj_dp.search(cr, uid, [('fecha_fin','=',argument_search)])

		fecha_fin  = obj_dp.read(cr,uid,search_fin,context=context)
		#=========================================================================
		
		if str(item) == "1":

			if not fecha_ini:
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe la Feha de Inicio no existe, intente de nuevo...",
				}

				values.update({
					
					'fecha_inicio' : None,
					})
		if str(item) == "2":

			if not fecha_fin:
				mensaje = {
						'title'   : "Cambio de estátus",
						'message' : "Disculpe la Feha de Finalizacion no existe, intente de nuevo...",
				}

				values.update({
					
					'fecha_fin' : None,
					})

		return {'value' : values,'warning' : mensaje}

	def search_dep(self, cr, uid, ids, argument_search,item, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('gestion.eventos')
		
		#======================== Busqueda por código ============================
		dep        = obj_dp.search(cr, uid, [('institucion','=',argument_search)])

		depart     = obj_dp.read(cr,uid,dep,context=context)
		#=========================================================================
		if str(item) == "3":

			if not depart:
				mensaje = {
						'title'   : "Busqueda por Departamento",
						'message' : "No existen registros para este Departamento, intente de nuevo...",
				}

				values.update({
					
					'institucion' : None,
					})

		return {'value' : values,'warning' : mensaje}

	#################################################################
	# METODO PARA GERAR LOS DIFERENTES REPORTES DE GESTION DE EVENTOS
	#################################################################
	
	def gestion_emitir_detallado(self, cr, uid, ids, context=None):
		# Instancia de la clase heredada L es horizontal y P es vertical
		campo = self.read(cr, uid, ids, context=context)[0] # Lectura del objeto propio
		# REALIZAMOS LA LECTURA DE LOS VALORES A FILTRAR
		
		for gestion in self.browse(cr, uid, ids, context=None):
			cantidad   = gestion.cantidad # CANTIDAD DE REGISTROS A MOSTRAR
			mostrar    = gestion.asc_desc # ORDEN DE BUSQUEDA
			fec_inicio = gestion.fecha_inicio # CAPTURA DE FECHA DE INICIO DEL EVENTO
			fec_fin    = gestion.fecha_fin # CAPTURA DE FECHA DE FIN DEL EVENTO
			user       = gestion.user.login # SE CAPTURA EL USUARIO LOGEADO
			ins        = gestion.institucion.id

		if str(mostrar) == "todos": # CONDICIONAL PARA TODOS LOS REGISTROS
			cabezera = "Detallado de Eventos"
			item     = "todos"
			#print "FILTRO PARA TODOS LOS EVENTOS"
			cr.execute('SELECT ge.name, mun.name, par.name, g.create_date, g.actividad,g.participantes,g.responsable,g.status,g.direccion,g.hora_inicio,g.hora_fin,g.inicio,g.fin,g.fecha_inicio,g.fecha_fin FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge, res_country_municipality AS mun, res_country_parish AS par WHERE g.institucion=ge.id AND g.municipio=mun.id AND g.parroquia=par.id')

		elif str(mostrar) == "fechas": # CONDICIONAL PARA TODOS LA BUSQUEDA DE FECHAS FIN / INICIO
			cabezera = "Detallado de Eventos por Fehas"
			item     = "fechas"
			if not campo['fecha_inicio']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la Fecha de Inicio..."))
			elif not campo['fecha_fin']:
					raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la Fecha de Fin..."))		
			else:
				cr.execute('SELECT ge.name, mun.name, par.name, g.create_date, g.actividad,g.participantes,g.responsable,g.status,g.direccion,g.hora_inicio,g.hora_fin,g.inicio,g.fin,g.fecha_inicio,g.fecha_fin FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge, res_country_municipality AS mun, res_country_parish AS par WHERE g.institucion=ge.id AND g.municipio=mun.id AND g.parroquia=par.id AND fecha_inicio='"'"+str(fec_inicio)+"'"' AND fecha_fin='"'"+str(fec_fin)+"'"'')


		elif str(mostrar) == "desc": # CONDICIONAL PARA LA BUSQUEDA DE LOS PRIMEROS REGISTROS
			cabezera = "Detallado  de Primeros Eventos"
			item     = "desc"
			if not campo['cantidad']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la cantidad de Actividades a mostrar..."))
			else:
				cr.execute('SELECT ge.name, mun.name, par.name, g.create_date, g.actividad,g.participantes,g.responsable,g.status,g.direccion,g.hora_inicio,g.hora_fin,g.inicio,g.fin,g.fecha_inicio,g.fecha_fin FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge, res_country_municipality AS mun, res_country_parish AS par WHERE g.institucion=ge.id AND g.municipio=mun.id AND g.parroquia=par.id ORDER BY status '+str(mostrar)+' LIMIT '+str(cantidad)+'')
		elif str(mostrar) == "asc": # CONDICIONAL PARA LA BUSQUEDA DE LOS ULTIMOS REGISTROS
			cabezera = "Detallado  de Últimos Eventos"
			item     = "asc"
			if not campo['cantidad']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe ingresar la cantidad de Actividades a mostrar..."))
			else:
				cr.execute('SELECT ge.name, mun.name, par.name, g.create_date, g.actividad,g.participantes,g.responsable,g.status,g.direccion,g.hora_inicio,g.hora_fin,g.inicio,g.fin,g.fecha_inicio,g.fecha_fin FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge, res_country_municipality AS mun, res_country_parish AS par WHERE g.institucion=ge.id AND g.municipio=mun.id AND g.parroquia=par.id ORDER BY status '+str(mostrar)+' LIMIT '+str(cantidad)+'')
		elif str(mostrar) == "departamento": # CONDICIONAL PARA TODOS LOS REGISTROS
			cabezera = "Detallado Por Departamento"
			item     = "departamento"
			if not campo['institucion']:
				raise osv.except_osv(_("Warning!"), _("Disculpe debe seleccionar el Departamento..."))
			else:
				cr.execute('SELECT ge.name, mun.name, par.name, g.create_date, g.actividad,g.participantes,g.responsable,g.status,g.direccion,g.hora_inicio,g.hora_fin,g.inicio,g.fin,g.fecha_inicio,g.fecha_fin FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge, res_country_municipality AS mun, res_country_parish AS par WHERE g.institucion=ge.id AND g.municipio=mun.id AND g.parroquia=par.id AND institucion='"'"+str(ins)+"'"'')
				
				# print "PROCESO DE DATOS: "+str(cr.fetchall())

		pdf = pdf_class.Detallado(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		pdf.set_author('ING JESUS LAYA')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		
		#####################################################################
		#		ESTRUCTURA PRINCIPAL DEL XSL ENCABEZADO
		#####################################################################
		style0 = xlwt.easyxf('font: name Times New Roman, colour black, bold on')
		style1 = xlwt.easyxf('',num_format_str='D-M-YY')
		wb = xlwt.Workbook()
		ws1 = wb.add_sheet('Cierre de Nomina',cell_overwrite_ok=True)
		ws1.write(1, 0, 'MUNICIPIO',style0)
		ws1.write(1, 1, 'PARROQUIA',style0)
		ws1.write(1, 2, 'DIRECCION',style0)
		ws1.write(1, 3, 'ACTIVIDAD',style0)
		ws1.write(1, 4, 'PARTICIPANTES',style0)
		ws1.write(1, 5, 'INSTITUCION / GERENCIA',style0)
		ws1.write(1, 6, 'RESPONSABLE',style0)
		ws1.write(1, 7, 'ESTATUS',style0)
		ws1.write(1, 8, 'FECHA',style0)
		ws1.write(1, 9, 'HORA',style0)
		ws1.write(1, 10, 'HORA DE INICIO',style0)
		ws1.write(1, 11, 'HORA DE FINALIZACION',style0)
		ws1.write(1, 12, 'FECHA DE INICIO',style0)
		ws1.write(1, 13, 'FECHA DE FINALIZACION',style0)
		
		can_1 = 0
		can_2 = 0
		can_3 = 0
		can_4 = 0
		can_5 = 0
		can_6 = 0
		x = 0
		contador = 1
		for detallado in cr.fetchall():
			
			#print "NUMERO DE REGISTROS DE GESTION DE EVENTOS: "+str(contador)

			institucion     = detallado[0].encode('UTF-8').decode('UTF-8') # INSTITUCION
			municipio       = detallado[1].encode('UTF-8').decode('UTF-8') # MUNICIPIO
			parroquia       = detallado[2].encode('UTF-8').decode('UTF-8') # PARROQUIA
			actividad       = detallado[4].encode('UTF-8').decode('UTF-8') # ACTIVIDAD
			participantes   = detallado[5].encode('UTF-8').decode('UTF-8') # PARTICIPANTES
			responsable     = detallado[6].encode('UTF-8').decode('UTF-8') # RESPONSABLE
			#status         = detallado[7] # STATUS
			fecha_actual    = detallado[3].split(' ')
			hora            = detallado[3].split('.')
			fecha           = format_fecha(fecha_actual[0])
			horas           = hora[0].split(' ')
			hora_actual     = horas[1]
			direccion       = detallado[8].encode('UTF-8').decode('UTF-8')
			fecha_de_inicio = detallado[9]
			fecha_de_fin    = detallado[10]
			inicio          = detallado[11]
			fin             = detallado[12]
			fec_ini         = format_fecha(detallado[13])
			fec_fi          = format_fecha(detallado[14])
			
			if int(inicio) == 1:
				 ini = "AM"
			else:
				ini = "PM"
				 
			if int(fin) == 2:
				 fi = "PM"
			else:
				fi = "AM"
				
				 
				
			if int(detallado[7]) == 1:
				status = "Pendiente"
				can_1  += len(detallado[7])
			if int(detallado[7]) == 2:
				status = "Realizado"
				can_2  += len(detallado[7])
			if int(detallado[7]) == 3:
				status = "Pospuesto"
				can_3  += len(detallado[7])
			if int(detallado[7]) == 4:
				status = "Reprogramado"
				can_4  += len(detallado[7])
			if int(detallado[7]) == 5:
				status = "Atrasado"
				can_5  += len(detallado[7])
			if int(detallado[7]) == 6:
				status = "Cancelado"
				can_6  += len(detallado[7])
			
			#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			pdf.set_font('Arial','B',15)
			pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
			pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	
			pdf.ln(10)
	
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
			
			pdf.cell(260,5,"DIRECCIÓN DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','B',9)
			pdf.cell(100,5,"Municipio: "+municipio,'LTB',0,'L',1)
			pdf.cell(100,5,"Parroquia: "+parroquia,'LTB',0,'L',1)
			pdf.cell(30,5,"Fecha: "+fecha,'LTB',0,'L',1)
			pdf.cell(25,5,"Hora: "+hora_actual,'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.cell(5,5,"".decode("UTF-8"),'BTR',1,'L',1)
			pdf.set_font('Arial','B',9)
			pdf.cell(217,5,"Dirección: ".decode("UTF-8")+direccion,'LTB',0,'L',1)
			pdf.set_font('Arial','',8)
			pdf.set_font('Arial','B',9)
			pdf.set_font('Arial','',8)
			pdf.cell(43,5,"".decode("UTF-8"),'TBR',1,'L',1)
	
			pdf.set_font('Arial','B',9)
	
			pdf.ln(5)
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',10)
	
			pdf.cell(260,5,"CARACTERÍSTICA DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
	
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.set_font('Arial','b',8)
	
			pdf.cell(230,5,"Actividad".decode("UTF-8"),'LTBR',0,'L',1)
			pdf.cell(30,5,"Participantes: ".decode("UTF-8")+participantes,'LTBR',1,'L',1)
	
			pdf.cell(260,10,actividad,'LTBR',1,'L',1)
	
			pdf.cell(150,10,"Institución / Gerencia: ".decode("UTF-8")+institucion,'LTBR',0,'L',1)
			pdf.cell(60,10,"Responsable: ".decode("UTF-8")+responsable,'LTBR',0,'L',1)
			pdf.cell(50,10,"Estátus: ".decode("UTF-8")+status,'LTBR',1,'L',1)
			
			if contador % 2 == 0:
				pdf.add_page() # AÑADE UNA NUEVA PAGINACION Y ESTABLECE DOS (2) REGISTROS POR PAGINA

			################################################################
			
			ws1.write(x+2, 0, municipio)
			ws1.write(x+2, 1, parroquia)
			ws1.write(x+2, 2, direccion)
			ws1.write(x+2, 3, actividad)
			ws1.write(x+2, 4, participantes)
			ws1.write(x+2, 5, institucion)
			ws1.write(x+2, 6, responsable)
			ws1.write(x+2, 6, responsable)
			ws1.write(x+2, 7, status)
			ws1.write(x+2, 8, fecha)
			ws1.write(x+2, 9, hora_actual)
			ws1.write(x+2, 10, fecha_de_inicio+" "+str(ini))
			ws1.write(x+2, 11, fecha_de_fin+" "+str(fi))
			ws1.write(x+2, 12, fec_ini)
			ws1.write(x+2, 13, fec_fi)
			
			x = x + 1 # ACUMULADOR DE LA DATA
			contador = contador + 1
			
		########################################################################
		#          CONSTRUCCION DE LA LEYENDA DE LOS TIPOS DE EVENTOS
		########################################################################
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.ln(5)
		pdf.cell(60,5,"TOTAL ACTIVIDADES".decode("UTF-8"),'LTBR',0,'C',1)

		pdf.ln(5)
		pdf.set_font('Arial','',8)
		pdf.set_text_color(0,0,0)
		pdf.set_fill_color(255,255,255)
		pdf.cell(20,4,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Eventos".decode("UTF-8"),'LTBR',1,'C',1)
	
		# Pendientes
		pdf.cell(20,4,str(can_1),'LTBR',0,'C',1)
		pdf.cell(40,4,"Pendientes".decode("UTF-8"),'LTBR',1,'C',1)
		# Realizadas
		pdf.cell(20,4,str(can_2),'LTBR',0,'C',1)
		pdf.cell(40,4,"Realizados".decode("UTF-8"),'LTBR',1,'C',1)
		# Postpuestos
		pdf.cell(20,4,str(can_3),'LTBR',0,'C',1)
		pdf.cell(40,4,"Pospuestos".decode("UTF-8"),'LTBR',1,'C',1)
		# Reprogramado
		pdf.cell(20,4,str(can_4),'LTBR',0,'C',1)
		pdf.cell(40,4,"Reprogramados".decode("UTF-8"),'LTBR',1,'C',1)
		# Atrasado
		pdf.cell(20,4,str(can_5),'LTBR',0,'C',1)
		pdf.cell(40,4,"Atrasados".decode("UTF-8"),'LTBR',1,'C',1)
		# Cancelado
		pdf.cell(20,4,str(can_6),'LTBR',0,'C',1)
		pdf.cell(40,4,"Cancelados".decode("UTF-8"),'LTBR',1,'C',1)

		########################################################################
		pdf.ln(5)
		pdf.set_x(100)
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		
		dia   = time.strftime('%d')
		mes   = time.strftime('%B')
		anyo  = time.strftime('%Y')
		fecha = dia+" de "+mes+" "+anyo
		
		title     = cabezera.upper()+ "("+fecha.upper()+") Usuario ".upper()+str(user).upper()+" "".pdf"
		title_xls = cabezera.upper()+ "("+fecha.upper()+")Usuario ".upper()+str(user).upper()+".xls"
		
		wb.save('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title_xls)
		archivo_xls = open('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title_xls)
		
		#~ wb.save('openerp/addons/gestion_eventos/reportes/'+title_xls)
		#~ archivo_xls = open('openerp/addons/gestion_eventos/reportes/'+title_xls)
		
		pdf.output('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title,'F')
		documento = open('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title) # Apertura del documento
		
		#~ pdf.output('openerp/addons/gestion_eventos/reportes/'+title,'F')
		#~ documento = open('openerp/addons/gestion_eventos/reportes/'+title) # Apertura del documento
		
		# Guardamos el archivo pdf en gestion.eventos
		self.pool.get('ir.documento').create(cr, uid, {
			'name': title,
			'res_name': title,
			'datas': base64.encodestring(documento.read()),
			'datas_fname': title,
			'res_model': 'gestion.eventos (Gestión de Eventos)',
			'description': title,
			'item': item,
			}, context=context)
		
		self.pool.get('ir.documento').create(cr, uid, {
			'name': title_xls,
			'res_name': title_xls,
			'datas': base64.encodestring(archivo_xls.read()),
			'datas_fname': title_xls,
			'res_model': 'gestion.eventos (Gestión de Eventos)',
			'description': title_xls,
			'item': item,
			}, context=context)
		#################################################################
	_columns = {

		'cantidad': fields.char(string="Cantidad", required = False),
		'asc_desc' : fields.selection([('todos','Todos'),('asc','Asendente'),('desc','Decendente'),('fechas','Fechas'),('departamento','Departamento')], string="Mostrar en Forma", required=True),
		'user': fields.many2one('res.users', 'Registrado por:', readonly=True), # Usuario logeado
		'fecha_inicio' : fields.date(string="Fecha Inicio", required=False),
		'fecha_fin' : fields.date(string="Fecha Fin", required=False),
		'institucion' : fields.many2one("gestion.inst.gerencia", "Institución / Gerencia", required = False),
	}

	_defaults = {
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}
# FORMATEAR FECHA (FUNCION GLOBAL PARA EL FORMATO DE FECHAS
def format_fecha(fecha):
	date = fecha.split("-")
	nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
	return nueva_fecha
