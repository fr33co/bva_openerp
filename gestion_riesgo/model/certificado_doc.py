from openerp.osv import osv, fields
class certificadodoc(osv.Model):
	_name = "certificado.doc"
        
          
	_columns = {
	    'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"),
            'num_certificado' : fields.char(string="Numero de certificado de Refugiado",size=100,),
            'descripcion' : fields.text(string="Descripcion",size=900, required=True),
	}
        
        
        
        def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('certificado.doc')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_certificado desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['num_certificado'], context=context)
			num_certificado = rd_id[0]['num_certificado']
			numero = num_certificado[8]
			str_number = str(int(numero)+1)
			num_certificado = str('GRCR2014-'+str_number)
	    else:
	        num_certificado = 'GRCR2014-1'
	    return num_certificado
	_defaults = {
	    'num_certificado' : _get_last_id
            }