from openerp.osv import osv, fields
class gestionsolicitudes(osv.Model):
	_name = "gestion.solicitudes"
	_rec_name = "id_solicitud"



	  
	_columns = {
	    'id_solicitud' : fields.char(string="Numero de Solicitud",size=25, required=True),
	    'cedula' : fields.integer(string="Cedula Solicitante",size=25, required=True),
	    'fecha' : fields.date(string="Fecha de Solicitud",size=25, required=True),
	    'tipo' : fields.selection([('inspeccion','Inspeccion'),('constancia','Constancia'),('certificado','Certificado')],string="Tipo de Documento",size=100, required=True),
	    'motivo' : fields.text(string="Motivo de Solicitud",size=300, required=True),
	    'observacion' : fields.text(string="Observaciones",size=300),
	    'estatus' : fields.selection([('pendiente','Pendiente Elaboracion'),('firma','Espera de Firma'),('entregado','Entregado')],string="Estatus",size=100, required=True),
	}

	'''
	asignar numeracion a las solicitudes
	'''

	def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('gestion.solicitudes')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='id_solicitud desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['id_solicitud'], context=context)
			id_documento = rd_id[0]['id_solicitud']
			numero = id_documento[4]
			str_number = str(int(numero)+1)
			id_solicitud = str('GRS-'+str_number)
	    else:
	        id_solicitud = 'GRS-1'
	    return id_solicitud
	_defaults = {
	    'id_solicitud' : _get_last_id
	}
