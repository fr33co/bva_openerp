# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class Seleccion(osv.Model):
	_name = 'becados.solicitudes'
	
	_order = 'solicitante'
	
	_rec_name = 'solicitante'
	
	def action_demanda_inicial(self, cr, uid, ids, context=None):
		#ajuste en estado de Demanda inicial de beca
		return self.write(cr, uid, ids, {'stage_id':'Demanda inicial de beca'}, context=context)
		
	def action_primera_entrevista(self, cr, uid, ids, context=None):
		#ajuste en estado de Primera entrevista
		return self.write(cr, uid, ids, {'stage_id':'Primera entrevista'}, context=context)
		
	def action_segunda_entrevista(self, cr, uid, ids, context=None):
		#ajuste en estado de Segunda entrevista
		return self.write(cr, uid, ids, {'stage_id':'Segunda entrevista'}, context=context)
		
	def action_beca_propuesta(self, cr, uid, ids, context=None):
		#ajuste en estado de Beca propuesta
		return self.write(cr, uid, ids, {'stage_id':'Beca propuesta'}, context=context)

	_columns = {
		'cedula' : fields.integer(string="Cédula", size=8, required=True),
		'solicitante': fields.char(string="Nombres y Apellidos", size=100, required = True),
		'email' : fields.char(string="Correo", required=False),
		'telefono' : fields.char(string="Teléfono", required=False),
		'movil' : fields.char(string="Móvil", required=False),
		'grado_instruc' : fields.many2one("becados.gradoinstruccion", "Grado de Instrucción", required=False),
		'direccion' : fields.char(string="Dirección", size=256, required=False),
		'experiencia' : fields.char(string="Años de experiencia",required=False),
		'sede' : fields.many2one("becados.sedes", "Sede", required = False),
		'responsable' : fields.char(string="Responsable", required=False),
		'prox_accion' : fields.date(string="Próxima acción", required=False),
		'apreciacion' : fields.selection((('Malo','Malo'),('Promedio','Promedio'),('Bueno','Bueno'),('Muy Bueno','Muy Bueno'),('Excelente','Excelente')), "Apreciación", required=False),
		'origen' : fields.selection((('externo','Recomendación Externa'),('interno','Recomendación Interna')), "Origen", required=False),
		'recomendacion' : fields.char(string="Recomendado por", size=100, required=False),
		'resumen' : fields.text(string="Resumen de la Solicitud", required=False),
		'fecha_solicitud' : fields.date(string="Fecha de la Solicitud", required=False),
		'stage_id' : fields.selection((('Demanda inicial de beca','Demanda inicial de beca'),('Primera entrevista','Primera entrevista'),('Segunda entrevista','Segunda entrevista'),('Beca propuesta','Beca propuesta')), "Estado", required=True),
	}
	
	_defaults = {
		'stage_id' : 'Demanda inicial de beca',
		'fecha_solicitud' : lambda *a: time.strftime("%Y-%m-%d"),
	}

