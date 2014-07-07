# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class organos_entes(osv.Model):

	_name = "organos.entes"
	_rec_name = 'nombre_ente'
	
	_columns = {
		'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
		'f_solicitud': fields.char('Fecha de Elaboración:', readonly=True, required=True),
		'nombre_ente' : fields.char(string="Nombre de la Acción Específica", required=False),
		'siglas' : fields.char(string="Unidad de Medida", required=False),
		'correo' : fields.char(string="Cantidad", required=False),
		'tipo': fields.selection([('1','Órgano / Secretaria'), ('2','Ente / Empresa')], string="Tipo Órgano/Ente"),
		't_estructura':fields.many2one('tipo.estructura', 'Tipo Estructura', ondelete='cascade', select=False),
		'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False),
		'c_adscrip' : fields.char(string="Código Adscripción", required=False),
		'c_act' : fields.char(string="Código Actividad", required=False),
		'nom_responsable' : fields.char(string="Nombre del Responsable", required=False),
		'cargo' : fields.char(string="Cargo", required=False),
		'telefono' : fields.char(string="Teléfono", required=False),
		'ci' : fields.char(string="C.I.", required=False),
		'direccion' : fields.char(string="Dirección", required=False),
	}
	_defaults = {
		'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
		'user_register': lambda s, cr, uid, c: uid,
	}    