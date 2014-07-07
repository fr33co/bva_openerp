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

class Gestion_eventos(osv.Model):
	
	_name = 'gestion.eventos'
	_rec_name = 'actividad'
	
	
	def emitir_foto(self, cr, uid, ids, context=None):
		
		pdf=pdf_class.Fotos(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

		pdf.set_author('ING JESUS LAYA')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		
		#############################################################
		#                 CAPTURA DE LOS DATOS
		#############################################################
		obj = ""
		for foto in self.browse(cr, uid, ids, context=None):
			
			mun         = foto.municipio.name
			parr        = foto.parroquia.name
			direccion   = foto.direccion
			actividad   = foto.actividad
			part        = foto.participantes
			institucion = foto.institucion.name
			resp        = foto.responsable
			status      = foto.status
			observacion = foto.observacion
			foto_a      = foto.foto_1
			foto_b      = foto.foto_2
			foto_c      = foto.foto_3

		open_doc = open(foto_a, "wb+")

		print "ARCHIVO: "+str(open_doc)

		# 	if observacion is False:
		# 		observacion = ""
		# 	else:
		# 		obj = aceptar(observacion)
			
		# if str(status) == "1":
		# 	status = "Pendiente"
				
		# if str(status) == "2":
		# 	status = "Realizado"
			
		# if str(status) == "3":
		# 	status = "Pospuesto"
			
		# if str(status) == "4":
		# 	status = "Reprogramado"
			
		# if str(status) == "5":
		# 	status = "Atrasado"
			
		# if str(status) == "6":
		# 	status = "Cancelado"
			

		# dia   = time.strftime('%d')
		# mes   = time.strftime('%m')
		# ano   = time.strftime('%Y')
		# fecha = dia+"/"+mes+"/"+ano
		# #############################################################

		# pdf.ln(7)
		
		# pdf.set_fill_color(199,15,15)
		# pdf.set_text_color(255,255,255)
		# pdf.set_font('Arial','B',10)
		# pdf.cell(190,5,"DIRECCIÓN DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
		# pdf.set_fill_color(255,255,255)
		# pdf.set_text_color(24,29,31)
		# pdf.set_font('Arial','B',9)
		# pdf.cell(70,5,"Municipio: "+aceptar(mun),'LTB',0,'L',1)
		# pdf.cell(90,5,"Parroquia: "+aceptar(parr),'LTB',0,'L',1)
		# pdf.cell(25,5,"HORA:".decode("UTF-8"),'LTB',0,'L',1)
		# pdf.set_font('Arial','',8)
		# pdf.cell(5,5,"".decode("UTF-8"),'BTR',1,'L',1)
		# pdf.set_font('Arial','B',9)
		# pdf.cell(147,5,"Dirección: ".decode("UTF-8")+aceptar(direccion),'LTB',0,'L',1)
		# pdf.set_font('Arial','',8)
		# pdf.set_font('Arial','B',9)
		# pdf.set_font('Arial','',8)
		# pdf.cell(43,5,"".decode("UTF-8"),'TBR',1,'L',1)
		
		# pdf.set_font('Arial','B',9)
		
		# pdf.ln(5)
		# pdf.set_fill_color(199,15,15)
		# pdf.set_text_color(255,255,255)
		# pdf.set_font('Arial','B',10)
		
		# pdf.cell(190,5,"CARACTERÍSTICA DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
		
		# pdf.set_fill_color(255,255,255)
		# pdf.set_text_color(24,29,31)
		# pdf.set_font('Arial','b',8)
		
		# pdf.cell(160,5,"Actividad".decode("UTF-8"),'LTBR',0,'L',1)
		# pdf.cell(30,5,"Participantes: "+part,'LTBR',1,'L',1)
		
		# pdf.cell(190,10,actividad,'LTBR',1,'L',1)
		
		# pdf.cell(100,10,"Institución / Gerencia: ".decode("UTF-8")+aceptar(institucion),'LTBR',0,'L',1)
		# pdf.cell(60,10,"Responsable: "+aceptar(resp),'LTBR',0,'L',1)
		# pdf.cell(30,10,"Estátus: ".decode("UTF-8")+status,'LTBR',1,'L',1)
		

		
		
		# ########################################################################
		# pdf.set_fill_color(199,15,15)
		# pdf.set_text_color(255,255,255)
		# pdf.set_font('Arial','B',10)
		# pdf.cell(190,5,"OBSERVACIONES DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
		
		# pdf.set_fill_color(255,255,255)
		# pdf.set_text_color(24,29,31)
		# pdf.set_font('Arial','b',8)
		
		# pdf.cell(190,15,obj,'LTBR',0,'L',1)
		# ########################################################################
		
		
		# pdf.ln(15)
		# pdf.set_fill_color(199,15,15)
		# pdf.set_text_color(255,255,255)
		# pdf.set_font('Arial','B',10)
		
		# pdf.cell(190,5,"FOTOS ADJUNTAS".decode("UTF-8"),'LTBR',1,'C',1)
		
		# pdf.set_fill_color(255,255,255)
		# pdf.set_text_color(24,29,31)
		# pdf.set_font('Arial','b',8)
		
		# pdf.cell(63.3,70,foto_a,'LTBR',0,'L',1)
		# pdf.cell(63.3,70,"FOTO 2".decode("UTF-8"),'LTBR',0,'L',1)
		# pdf.cell(63.3,70,"FOTO 3".decode("UTF-8"),'LTBR',1,'L',1)
		
		
		# dia   = time.strftime('%d')
		# mes   = time.strftime('%B')
		# anyo  = time.strftime('%Y')
		# fecha = dia+" de "+mes+" "+anyo
		
		# title = "Foto del Evento ("+fecha+").pdf"
		
		# #~ pdf.output('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title,'F')
		# #~ documento = open('/home/administrador/openerp70/modules/gestion_eventos/reportes/'+title) # Apertura del documento
		
		# pdf.output('openerp/addons/gestion_eventos/reportes/'+title,'F')
		# documento = open('openerp/addons/gestion_eventos/reportes/'+title) # Apertura del documento
		
		# # Guardamos el archivo pdf en gestion.eventos
		# self.pool.get('ir.documento').create(cr, uid, {
		# 	'name': title,
		# 	'res_name': title,
		# 	'datas': base64.encodestring(documento.read()),
		# 	'datas_fname': title,
		# 	'res_model': 'gestion.eventos (Foto del Evento)',
		# 	'description': title,
		# 	'item': "foto",
		# 	}, context=context)
	
	
	# METODO PARA TRAER EL NOMBRE DEL GERENTE ADSCRITO
	def search_ins_geren(self, cr, uid, ids, argument_search, context=None): # Proceso de busqueda de un manager(Gerente)

		values = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('gestion.inst.gerencia')
		
		#======================== Busqueda por Gerencia ============================

		search_obj_code = obj_dp.search(cr, uid, [('id','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		#=========================================================================
		if not datos_code[0]['gerente']:
			
			values.update({
				
				'responsable' : None,
				})
		else:
			
			values.update({
				
				'responsable' : datos_code[0]['gerente'],
				})

		return {'value' : values}


	# METODO VALIDADOR PARA ESTABLECER INICIO Y FIN DE LAS FECHAS DEL EVENTO
	def search_date_ini(self, cr, uid, ids, fecha, context=None):
		values = {}
		mensaje = {}
		
		if not fecha:
			
			return values
		
		now = datetime.now().strftime('%Y-%m-%d')
		
		if fecha < now:
			
			mensaje = {
					'title'   : "Eventos",
					'message' : "Disculpe, no puede seleccionar una fecha anterior al actual, intente de nuevo...",
			}

			values.update({
				'fecha_inicio' : None,
				})

		return {'value' : values,'warning' : mensaje}

	def search_date_fin(self, cr, uid, ids, fecha, context=None):
		values = {}
		mensaje = {}
		
		if not fecha:
			
			return values
		
		now = datetime.now().strftime('%Y-%m-%d')
		
		if fecha < now:
			
			mensaje = {
					'title'   : "Eventos",
					'message' : "Disculpe, no puede seleccionar una fecha posterior a la fecha de inicio, intente de nuevo...",
			}

			values.update({
				'fecha_fin' : None,
				})

		return {'value' : values,'warning' : mensaje}

	# ESTATUS REALIZADO
	def gestion_realizado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '2'}, context=context)
	# ESTATUS SUSPENDIDO
	def gestion_suspendido(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '3'}, context=context)
	# ESTATUS REPROGRAMADO
	def gestion_reprogramado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '4'}, context=context)
	# ESTATUS ATRASADO
	def gestion_atrasado(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '5'}, context=context)
	########################################################################
	# ESTATUS CANCELADO
	def gestion_cancelar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'status': '6'}, context=context)


	_columns = {
		######################################################################################
		# GESTION DE EVENTOS
		######################################################################################
		'institucion' : fields.many2one("gestion.inst.gerencia", "Institución / Gerencia", required = True),
		'responsable' : fields.char(string="Responsable", size=150, required=False),
		'actividad' : fields.char(string="Actividad", size=256, required=True),
		'fecha_inicio' : fields.date(string="Fecha Inicio", required=True),
		'fecha_fin' : fields.date(string="Fecha Fin", required=True),
		'hora_inicio' : fields.char(string="Hora Inicio", size=25, required=True),
		'hora_fin' : fields.char(string="Hora Fin", size=25, required=True),
		'direccion' : fields.text(string='Dirección', required=False),
		'nacionalidad' : fields.many2one("res.country", "Nacionalidad", required = False),
		'estado' : fields.many2one("res.country.state", "Estado", required = False, select="0"),
		'ciudad' : fields.many2one("res.country.city", "Ciudad", required = False, select="0"),
		'municipio' : fields.many2one("res.country.municipality", "Municipio", required = True),
		'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = False, select="0"),
		'participantes' : fields.char(string="Participantes", size=4, required=True),
		'observacion' : fields.text(string='Observación', required=False),
		'recursos': fields.text(string="Recursos", size=500, required=False),
		'status_logistico' : fields.selection([('1','Aprobado totalmente'),('2','Aprobado Parcialmente'),('3','No Aprobado')], string="Estado", required=False),
		'observacion_rl': fields.text(string="Observaciones", size=500, required=False),
		'si' : fields.boolean(string="Si"),
		'no' : fields.boolean(string="No"),
		'user': fields.many2one('res.users', 'Registrado por:', readonly=True), # Usuario logeado
		'descripcion' : fields.text(string='Descripciòn', required=False),
		'motivo' : fields.text(string='Motivo', required=False),
		'rep_event_si' : fields.boolean(string="Si"),
		'rep_event_no' : fields.boolean(string="No"),
		'status' : fields.selection([('1','Pendiente'),('2','Realizado'),('3','Pospuesto'),('4','Reprogramado'),('5','Atrasado'),('6','Cancelado')], string="Acción", required=False),
		'inicio' : fields.selection([('1','AM'),('2','PM')], string="Inicio", required=True),
		'fin' : fields.selection([('1','AM'),('2','PM')], string="Fin", required=True),
		'foto_1' : fields.binary("",help="Foto A"),
		'foto_2' : fields.binary("",help="Foto B"),
		'foto_3' : fields.binary("",help="Foto C"),
		'foto_4' : fields.binary("",help="Foto D"),
		######################################################################################
	}
	
	_defaults = {
		'nacionalidad' : 240, # Nacionalidad por defecto
		'estado' : 55, # Estado por defecto
		'ciudad' : 16, # Ciudad por defecto
		'status' : '1', # Estatus por defecto Pendiente
		'hora_inicio' : '00:00',
		'hora_fin' : '00:00',
		'user': lambda s, cr, uid, c: uid, # Captura del usuario logeado
	}

def aceptar(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
	return result

def format_fecha(fecha):
	date = fecha.split("-")
	nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
	return nueva_fecha

def redondear(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida
