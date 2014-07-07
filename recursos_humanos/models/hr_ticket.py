# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

import urllib2, urllib
import time
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
#####################################################
import re # Importar re para eliminar aceptos
import unicodedata #Importar re para eliminar aceptos
import httplib
#####################################################

from openerp.osv import osv, fields

class Cesta_ticket(osv.Model):
	_name="hr.ticket"

	_order = 'status'
	
	_rec_name = 'nombres'
	
	_columns = {

		'cedula': fields.char(string = "Cédula", size = 256, required = False),
		'nombres': fields.char(string="Nombres y Apellidos", required = False),
		'fecha_ingreso': fields.date("Fecha de Ingreso", required=False),
		'monto': fields.char(string="Monto / Ticket", required = False),
		'ticket': fields.char(string="Can / Ticket", required = False),
		'monto_p': fields.char(string="Monto / Pagar", required = False),
		'tipo_recarga': fields.selection((('1','Targeta Electrónica'),('2','Pedido de Tickeras')), "Tipo de Recarga", required=False),
		'status': fields.selection([('1','Activo'),('5','Suspendido'),('7','Egresado')], string="Estado"),
		'class_personal' : fields.many2one("becados.clasper", "Personal", required = False),

	}

	_defaults = {
		#'codigo' :
		'status' : '1',
		
	}



