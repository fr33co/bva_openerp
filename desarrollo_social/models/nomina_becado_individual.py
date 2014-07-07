# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	_name="becados.nominaindividual"

	_order = 'codigo'
	
	_rec_name = 'codigo'
	
	#Función para la carga automática del monto de la asignación correspondiente al becado según el tipo de beca seleccionado
	def carga_monto(self, cr, uid, ids, tipo_beca, asignacion, cant_meses, context=None):
		
		valores = {}	
		
		if not tipo_beca:
			return valores
		
		#~ print tipo_beca
		
		#Seleccionamos el modelo de búsqueda
		modelo = self.pool.get('becados.tipobeca')		
		
		#Verificamos si la nómina individual del becado ya fue generada (se toma en cuenta el código)
		search_tipobeca = modelo.search(cr, uid, [('id','=',tipo_beca)])
		#~ print search_tipobeca
		
		if search_tipobeca:
			leer_tipobeca = modelo.read(cr, uid, search_tipobeca, context=context)
			
			if asignacion:
				if asignacion == "sin_asignacion":
					valores.update({
						'monto' : float(0),
					})
				elif asignacion == "beca_completa":  
					valores.update({
						'monto' : leer_tipobeca[0]['asignacion'],
					})
				elif asignacion == "media_beca":
					valores.update({
						'monto' : leer_tipobeca[0]['asignacion']/2,
					})
				elif asignacion == "bono_f":
					if cant_meses:
						bono_mes = (leer_tipobeca[0]['asignacion']*3)/12
						bono_total = bono_mes*int(cant_meses)
						valores.update({
							'monto' : leer_tipobeca[0]['asignacion']+bono_total,
						})
				else:
					valores.update({
						'monto' : leer_tipobeca[0]['asignacion'],
					})
		
		return {'value':valores}
	
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
		'codigo' : fields.char(string="Código", size=20, required=False),
		'becado': fields.many2one("hr.employee", "Becado", required = True, domain=[('categoria','=','1')]), #Anteriormente domain=[('categoria','=','1'),('status','=','1')]
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required=True),
		'asignacion' : fields.selection((('sin_asignacion','Sin Asignación'),('beca_completa','Beca Completa'),('media_beca','Media Beca'),('bono_f','Bono Fin de Año')), "Asignación", required=True), 
		'num_meses' : fields.selection((('1','Un Mes'),('2','Dos Meses'),('3','Tres Meses'),('4','Cuatro Meses'),('5','Cinco Meses'),('6','Seis Meses'),('7','Siete Meses'),('8','Ocho Meses'),('9','Nueve Meses'),('10','Diez Meses'),('11','Once Meses'),('12','Doce Meses')), "CantMeses", required=True),
		'monto' : fields.float(string="Monto", required=True), 
	}
	
	_defaults = {
		'anyo' : lambda *a: time.strftime("%Y"),
		'asignacion' : 'beca_completa',
		'num_meses' : '12',
	}
