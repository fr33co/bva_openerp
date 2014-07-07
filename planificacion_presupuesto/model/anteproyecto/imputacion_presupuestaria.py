# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class imputacion_presupuestaria(osv.Model):

	_name = "imputacion.presupuestaria"

	_columns = {
		'imputacion_ids':fields.many2one('imputacion.presupuestaria', 'imputacion_presupuestaria', ondelete='cascade', select=False),
		'codigo' : fields.char(string="Código", required=False),
		'partida_presu' : fields.char(string="Partida Presupuestaria", required=False),
		'trim_1' : fields.float(string="Trimestre I", required=False),
		'trim_2' : fields.float(string="Trimestre II", required=False),
		'trim_3' : fields.float(string="Trimestre III", required=False),
		'trim_4' : fields.float(string="Trimestre IV", required=False),
		'total_impu' : fields.float(string="Cantidad", required=False),
	}