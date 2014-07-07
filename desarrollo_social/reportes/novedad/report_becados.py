# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class order(report_sxw.rml_parse):

	def __init__(self, cr, uid, novedades_becados, context=None):
		super(order, self).__init__(cr, uid, novedades.becados, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.novedades', 'novedades.becados', 'addons/desarrollo_social/reportes/novedad/reportes.rml', parser=order)
