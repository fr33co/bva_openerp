# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class Nomina(osv.Model):
	
	'''Herenciando a hr.payslip (Nomina de Becado)'''
	
	_inherit = 'hr.payslip'
	
	_columns = {
		#'categoria' : fields.many2one('hr.employee.category', 'Categoría', required=True),
		'categoria' : fields.selection((('1','Becado'),('2','Empleado'),('3','Obrero'),('4','Coordinador_eje'),('5','Coordinador_sede')), "Categoria", required = False),
		'cedula' : fields.char(string="Cédula", size = 8, required=False),
		#~ 'asignacion': fields.float(string = "Asignación", required = False),
	}
	
	#~ _default = {
		#~ 'categoria' : 'Becados',
	#~ }
