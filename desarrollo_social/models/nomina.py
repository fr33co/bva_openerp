# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class Nomina(osv.Model):
	
	'''Herenciando a hr.payslip (Nomina de Becado)'''
	
	_inherit = 'hr.payslip'
	
	_columns = {
		'categoria' : fields.many2one('hr.employee.category', 'Categoría', required=True),
		'cedula' : fields.char(string="Cédula", size = 8, required=True),
	}
	
	#~ _default = {
		#~ 'categoria' : 'Becados',
	#~ }
