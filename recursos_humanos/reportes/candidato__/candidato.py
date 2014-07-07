# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class Candidato_employee(report_sxw.rml_parse):

	def __init__(self, cr, uid, hr_applicant, context=None):
		super(order, self).__init__(cr, uid, hr.applicant, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.candidato.empleado', 'hr.applicant', 'addons/recursos_humanos/reportes/candidato/candidato.rml', parser=Candidato_employee)
