# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class metas_accion_especifica(osv.Model):

	_name = "metas.especificas"

	_columns = {
		'metas_acc_espec':fields.many2one('actividades.trimestrales', 'metas_accion_especifica', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", required=False),
		'trim_1' : fields.float(string="I Trimestre", required=False),
		'trim_2' : fields.float(string="II Trimestre", required=False),
		'trim_3' : fields.float(string="III Trimestre", required=False),
		'trim_4' : fields.float(string="IV Trimestre", required=False),
		'total_trim' : fields.float(string="TOTAL", required=False),

	}