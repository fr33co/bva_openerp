# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class metas_financieras(osv.Model):

	_name = "metas.financieras"

	_columns = {
		'metas_ids':fields.many2one('metas.financieras', 'metas_financieras', ondelete='cascade', select=False),
		'nom_accion_metas' : fields.char(string="Nombre de la Acción Específica", required=False),
		'trim_1' : fields.float(string="Trimestre I", required=False),
		'trim_2' : fields.float(string="Trimestre II", required=False),
		'trim_3' : fields.float(string="Trimestre III", required=False),
		'trim_4' : fields.float(string="Trimestre IV", required=False),
		'total_meta' : fields.float(string="Cantidad", required=False),
	}

