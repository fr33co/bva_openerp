from openerp.osv import osv, fields
class infinspecciondoc(osv.Model):
	_name = "infinspeccion.doc"
        
          
	_columns = {
	    'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"),
            'num_infinspeccion' : fields.char(string="Numero de Informe de Inspeccion",size=100,),
            'descripcion' : fields.text(string="Descripcion",size=900, required=True),
	}
        
        
        
        def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('infinspeccion.doc')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_infinspeccion desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['num_infinspeccion'], context=context)
			num_infinspeccion = rd_id[0]['num_infinspeccion']
			numero = num_infinspeccion[11]
			str_number = str(int(numero)+1)
			num_infinspeccion = str('GRIINSP2014-'+str_number)
	    else:
	        num_infinspeccion = 'GRIINSP2014-1'
	    return num_infinspeccion
	_defaults = {
	    'num_infinspeccion' : _get_last_id
            }