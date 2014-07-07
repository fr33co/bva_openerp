# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class acciones_especificas(osv.Model):

	_name = "acciones.especificas"

	_columns = {
		'acciones_ids':fields.many2one('acciones.especificas', 'acciones_especificas', ondelete='cascade', select=False),
		'nombre_accion' : fields.char(string="Nombre de la Acción Específica", required=False),
		'unidad_medida' : fields.char(string="Unidad de Medida", required=False),
		#'unidad_medida' : fields.many2one('product.uom', 'Unidad de Medida',required=False),
		'cantidad' : fields.integer(string="Cantidad", required=False),
		'trim_i' : fields.float(string="Trimestre I", required=False),
		'trim_ii' : fields.float(string="Trimestre II", required=False),
		'trim_iii' : fields.float(string="Trimestre III", required=False),
		'trim_iv' : fields.float(string="Trimestre IV", required=False),
		'total' : fields.float(string="Cantidad", required=False),
	}