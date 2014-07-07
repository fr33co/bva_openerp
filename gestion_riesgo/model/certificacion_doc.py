from openerp.osv import osv, fields
class certificaciondoc(osv.Model):
	_name = "certificacion.doc"
        
          
	_columns = {
	    'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"),
            'num_certificacion' : fields.char(string="Numero de certificacion de Habitabilidad",size=100,),
            'descripcion' : fields.text(string="Descripcion",size=900, required=True),
	}
        
        
        
        def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('certificacion.doc')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_certificacion desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['num_certificacion'], context=context)
			num_certificacion = rd_id[0]['num_certificacion']
			numero = num_certificacion[8]
			str_number = str(int(numero)+1)
			num_certificacion = str('GRCH2014-'+str_number)
	    else:
	        num_certificacion = 'GRCH2014-1'
	    return num_certificacion
	_defaults = {
	    'num_certificacion' : _get_last_id
            }