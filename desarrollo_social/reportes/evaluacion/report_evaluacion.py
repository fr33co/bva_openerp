# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class Evaluacion(report_sxw.rml_parse):

	def __init__(self, cr, uid, evaluacion_becados, context=None):
		super(order, self).__init__(cr, uid, evaluacion.becados, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.evaluacion', 'evaluacion.becados', 'addons/desarrollo_social/reportes/evaluacion/reporte_evaluacion.rml', parser=Evaluacion)
