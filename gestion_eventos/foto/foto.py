# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class Foto(report_sxw.rml_parse):

	def __init__(self, cr, uid, gestion_eventos, context=None):
		super(order, self).__init__(cr, uid, gestion.eventos, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.foto', 'gestion.eventos', 'addons/gestion_eventos/foto/foto.rml', parser=Foto)
