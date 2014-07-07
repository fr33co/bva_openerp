# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class plan_de_la_patria(osv.Model):

	_name = "plan.patria"
	
	_rec_name ="plan_patria"	
	_columns = {
		
		'plan_patria' : fields.char(string="Plan de la Patria", required=True),
		
	}
	
class objetivos_historicos(osv.Model):

	_name = "objetivo.historico"

	_rec_name ="objetivo_historico"
	_columns = {
		
		'objetivo_historico' : fields.text(string="Objetivos Historicos", required=False),
		'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=True),
	}

class objetivos_nacionales(osv.Model):

	_name = "objetivo.nacional"
	_rec_name ="objetivo_nacional"
	_columns = {
		
		'objetivo_nacional' : fields.text(string="Objetivo Nacional", required=False),
		'objetivo_historico' : fields.many2one('objetivo.historico', 'Objetivos Historicos', required=True),
		'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=True),
	}



class objetivos_estrategicos(osv.Model):

	_name = "objetivo.estrategico"
	_rec_name ="objetivo_estrategico"
	_columns = {
		
		'objetivo_estrategico' : fields.text(string="Objetivos Estratégicos", required=False),
		'objetivo_nacional' : fields.many2one('objetivo.nacional', 'Objetivos Nacionales', required=True),
		'objetivo_historico' : fields.many2one('objetivo.historico', 'Objetivos Historicos', required=True),
		'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=True),
	}
	
class objetivos_generales(osv.Model):

	_name = "objetivo.general"
	_rec_name ="objetivo_general"
	_columns = {
		
		'objetivo_general' : fields.text(string="Objetivos Generales", required=False),
		'objetivo_estrategico' : fields.many2one('objetivo.estrategico', 'Objetivos Estratégico', required=True),
		'objetivo_nacional' : fields.many2one('objetivo.nacional', 'Objetivos Nacionales', required=True),
		'objetivo_historico' : fields.many2one('objetivo.historico', 'Objetivos Historicos', required=True),
		'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=True),
	}