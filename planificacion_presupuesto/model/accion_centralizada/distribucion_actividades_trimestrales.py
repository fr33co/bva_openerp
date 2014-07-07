# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class distribucion_actividades_trimestrales(osv.Model):

	_name = "actividades.trimestrales"

	_columns = {
		'act_trimestral_ids':fields.many2one('actividades.trimestrales', 'actividades_trimestrales', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", required=False),
		'trim_1' : fields.float(string="I Trimestre", required=False),
		'trim_2' : fields.float(string="II Trimestre", required=False),
		'trim_3' : fields.float(string="III Trimestre", required=False),
		'trim_4' : fields.float(string="IV Trimestre", required=False),
		'total_trim' : fields.float(string="TOTAL", required=False),

	}