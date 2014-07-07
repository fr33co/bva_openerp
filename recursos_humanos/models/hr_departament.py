# -*- coding: utf-8 -*-
import time # Necesario para las funciones de Fecha

from datetime import date
from openerp.osv import fields, osv

class Departament(osv.Model):
	
	'''Herenciando a hr.department (Departamento)'''
	
	_inherit = 'hr.department'
	
	_columns = {
		'cod' : fields.char(string="Código", size = 20),
		'gerente' : fields.many2one("res.users", "Gerente", required = False),
	}

