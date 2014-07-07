# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Sede(osv.Model):
	_name="becados.sedes"

	_order = 'sede'
	
	_rec_name = 'sede'
	
	#~ def carga_cod_eje(self, cr, uid, ids, eje, context=None):
		#~ valores = {}
		#~ 
		#~ if not eje:
			#~ return valores
		#~ 
		#~ #Preparación del modelo donde se realizará la búsqueda
		#~ modelo1 = self.pool.get('becados.ejes')
		#~ 
		#~ #Ejecución de la búsqueda
		#~ busqueda1 = modelo1.search_count(cr, uid, [('id','=',eje)])
		#~ 
		#~ if busqueda1 > 0:
			#~ #Lectura de los datos hallados
			#~ busqueda_leer = modelo1.read(cr, uid, busqueda1, context=context)
			#~ 
			#~ #Carga de los datos que necesitamos
			#~ valores.update({
				#~ 'cod_eje' : busqueda_leer[0]['codigo'],
			#~ })
			#~ 
			#~ return {'value':valores}
			
			
	
	_columns = {
		'codigo' : fields.char(string="Código", size=10, required=False),
		#~ 'eje' : fields.many2one("becados.ejes", "Eje", required = True),
		#~ 'cod_eje' : fields.char(string="Codigo", size=5, required = False),
		'eje' : fields.selection((('001','Eje Centro'),('002','Eje Costa'),('003','Eje Este'),('004','Eje Metro'),('005','Eje Sur')),"Eje",required=False),
		'sede': fields.char(string = "Sede", size = 150, required = True),
		'descripcion': fields.char(string = "Descripción", size = 150, required = True),
	}


