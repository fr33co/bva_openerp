# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class Seleccion(osv.Model):
	_name = 'becados.seleccion'

	#~ _order = 'solicitante'
	
	#~ _rec_name = 'solicitante'
	
	#------------------------------------------------------------------------------------------------------------
	#Función para cargar la cédula del solicitante registrado que coincida con el escogido del combo de selección
	def cedula_solicitante(self, cr, uid, ids, solicitante, context=None):
		valores = {}
		
		if not solicitante:
			return valores
		
		#Preparación del modelo donde se realizará la búsqueda
		modelo1 = self.pool.get('becados.solicitudes')
		
		#Ejecución de la búsqueda por cantidad
		busqueda1 = modelo1.search_count(cr, uid, [('id','=',solicitante)])
		
		if busqueda1 > 0:
			#Ejecución de la búsqueda por cantidad
			busqueda2 = modelo1.search(cr, uid, [('id','=',solicitante)])
			#Leer resultados de la segunda búsqueda y armar diccionario
			busqueda_leer = modelo1.read(cr, uid, busqueda2, context=context)
			
			#Carga del dato que necesitamos
			valores.update({
				'cedula' : busqueda_leer[0]['cedula'],
			})
			
			return {'value' : valores}
	
	#-------------------------------------------------------------------------------------------------------------		
	#Función para cargar el solicitante en el combo de selección según la cédula.
	def solicitante(self, cr, uid, ids, cedula, context=None):
		valores = {}
		
		if not cedula:
			return valores
		
		#Preparación del modelo donde se realizará la búsqueda
		modelo1 = self.pool.get('becados.solicitudes')
		
		#Ejecución de la búsqueda por cantidad
		busqueda1 = modelo1.search_count(cr, uid, [('cedula','=',cedula)])
		
		if busqueda1 > 0:
			#Ejecución de la búsqueda por cantidad
			busqueda2 = modelo1.search(cr, uid, [('cedula','=',cedula)])
			#Leer resultados de la segunda búsqueda y armar diccionario
			busqueda_leer = modelo1.read(cr, uid, busqueda2, context=context)
			
			#Carga del dato que necesitamos
			valores.update({
				'solicitante' : busqueda_leer[0]['id'],
			})
			
			return {'value' : valores}
	
	_columns = {
		'solicitante': fields.many2one("becados.solicitudes","Solicitante", domain=[('stage_id','=','Beca propuesta')],required = False),
		'cedula' : fields.char(string="Cédula del solicitante", size=8, required=False),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required = False),
		'asignacion' : fields.float(string="Asignación",required=False),
		'plan_pago' : fields.selection((('Mensual','Mensual'),('Trimestral','Trimestral'),('Semestral','Semestral'),('Anual','Anual'),('Semanal','Semanal'),('Bisemanal','Bisemanal'),('Bimensual','Bimensual')),"Pago Planificado",required=False),
		'notas' : fields.text(string="Notas", size=256, required=False),
	}
