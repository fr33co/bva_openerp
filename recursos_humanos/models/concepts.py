# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Concepts_payslip(osv.Model):
	_name="hr.concepts"

	_order = 'codigo asc'
	
	_rec_name = 'concepto'

	# MÉTODO DE BUSQUEDA PARA CONCEPTOS
	
	def search_hr_concepts(self, cr, uid, ids, argument_search, context=None):

		values = {}
		mensaje = {}
		
		if not argument_search:
			
			return values
		obj_dp = self.pool.get('hr.concepts')
		
		#======================== Busqueda por código ============================

		search_obj_code = obj_dp.search(cr, uid, [('codigo','=',argument_search)])

		datos_code = obj_dp.read(cr,uid,search_obj_code,context=context)
		
		#======================= Busqueda por descripcion ========================
		
		search_obj_concept = obj_dp.search(cr, uid, [('concepto','=',argument_search)])

		datos_concept = obj_dp.read(cr,uid,search_obj_concept,context=context)
		
		#=========================================================================		

		if datos_code:
			
			mensaje = {
					'title'   : "Código de Concepto",
					'message' : "Disculpe este codigo ya esta asignado al concepto "+datos_code[0]['concepto']+", intente de nuevo...",
			}

			values.update({
				
				'codigo' : None,

				})
								
		elif datos_concept:
			
			mensaje = {
					'title'   : "Descripción del Concepto",
					'message' : "Disculpe esta descripcion ya esta asignado al concepto "+datos_concept[0]['codigo']+", intente de nuevo...",
			}

			values.update({
				
				'concepto' : None,

				})
			
		return {'value' : values,'warning' : mensaje}
	
	_columns = {
		'codigo': fields.char(string = "Código", size = 4, required = True),
		'concepto': fields.text(string = "Concepto", size = 256, required = True),
		'frecuencia' : fields.selection((('1','Fijo'),('2','Esporádico'),('3','Prestamo'),('4','Acumulado')), "Frecuencia", required=False),
		'formula': fields.char(string = "Fórmula", size = 200, required = False),
		'items' : fields.many2one("presupuesto.partidas", "Partida presupuestaria", required = False),
		'f' : fields.selection((('1','Si'),('2','No')), "F", required=False),
		'mount': fields.char(string = "monto", size = 200, required = False),
		'c_integral': fields.boolean(string = "Cálculo integral"),
		'b_vac': fields.boolean(string = "Bono vacacional"),
		's_integral_n': fields.boolean(string = "Sueldo integral Nómina"),
	}

	_defaults = {
		#'codigo' : 
	}



