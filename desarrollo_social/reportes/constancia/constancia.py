# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class Constancia(report_sxw.rml_parse):

	def __init__(self, cr, uid, hr_employee, context=None):
		super(order, self).__init__(cr, uid, hr.employee, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.constancia', 'hr.employee', 'addons/desarrollo_social/reportes/constancia/constancia.rml', parser=Constancia)
