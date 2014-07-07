# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
import xlwt
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
import re
import unicodedata
import base64 #Necesario para la generación del .xls

# Clase Solicitud de reparacion de Canaima
class accion_centralizada(osv.Model):

    #  Nombre del objeto
    _name = "accion.centralizada"

    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

    """
    Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
    y se le suma 1.
    """
    def _get_last_id(self, cr, uid, ids, context = None):

        sfl_id       = self.pool.get('solicitud.soporte')
        srch_id      = sfl_id.search(cr,uid,[])
        rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
        if rd_id:
            id_documento = rd_id[-1]['c_solicitud']
            c_solicitud = id_documento[3:]
            last_id      = c_solicitud.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        else :
            str_number = '1'
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        return codigo
	
    """
    Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
    """
    def elimina_tildes(self, s):
    
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    """
    Metodo que trae la informacion de cada Ente/Organizacion.
    """
    def on_change_ente(self, cr, uid, ids, organismo, context=None):
        values = {}
        if not organismo:
            return values
        datos = self.pool.get('organos.entes').browse(cr, uid, organismo, context=context)
        values.update({
            'domicilio' : datos.direccion,
            'n_autoridad' : datos.nom_responsable,
            'cargo' : datos.cargo,
            'telefono': datos.telefono,
            'correo': datos.correo,
	    'cedula': datos.ci,
     
        })
        return {'value' : values}  



    _columns = {
        'c_solicitud' : fields.char(string="ID", size=255, required=True),
	'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
	'f_solicitud': fields.char('Fecha de Elaboración:', required=True),
	#Pestaña1
	'organismo': fields.many2one('organos.entes', 'Organismo/Ente/Empresa:', required=True),
        'n_autoridad': fields.char('Nombre de la Máxima Autoridad de la Institución:', required=True),
	'cedula': fields.char('C.I.:', required=True),
	'cargo': fields.char('Cargo:', required=True),
	'telefono': fields.char('Teléfono:', required=True),
	'correo': fields.char('Correo Electrónico:', required=True),
	#Pestaña2
	'poli_presu': fields.text('Política Presupuestaría:', required=True),
	#Pestaña3
	'n_accion_centra': fields.many2one('tipo.accion.centralizada', 'Nombre de la Acción Centralizada', required=True),
	'n_accion_espe': fields.many2one('tipo.accion.especifica', 'Nombre de la Acción Específica', required=True),
	#'n_accion_centra': fields.char('Nombre de la Acción Centralizada', required=True),
	#'n_accion_espe': fields.char('Nombre de la Acción Específica',  required=True),
	'unidad': fields.char('Unidad Ejecutora',  required=True),
	'responsable': fields.char('Responsable de la Unidad Ejecutora',  required=True),
	'cargo_acc': fields.char('Cargo:', required=True),
	'cedula_acc': fields.char('C.I.:', required=True),
	'correo_acc': fields.char('Correo Electrónico:', required=True),
	'telefono_acc': fields.char('Teléfono:', required=True),
	#pestaña4
	'distribucion_actividades':fields.one2many('distribucion.actividades', 'distribucion_ids',required=False),
	#pestaña5
	'actividades_trimestrales':fields.one2many('actividades.trimestrales', 'act_trimestral_ids',required=False),
	#pestañas6
	'meta_acc_esp_trim':fields.one2many('metas.especificas', 'metas_acc_espec',required=False),

        }

    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        #'c_solicitud': _get_last_id,
        'user_register': lambda s, cr, uid, c: uid,
  
    }     
