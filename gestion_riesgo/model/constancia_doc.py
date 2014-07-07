from openerp.osv import osv, fields
class constanciadoc(osv.Model):
	_name = "constancia.doc"
        
          
	_columns = {
	    'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"),
            'num_constancia' : fields.char(string="Numero de Constancia",size=100,),
            'descripcion' : fields.text(string="Descripcion",size=900, required=True),
	}
        
        
        
        def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('constancia.doc')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_constancia desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['num_constancia'], context=context)
			num_constancia = rd_id[0]['num_constancia']
			numero = num_constancia[7]
			str_number = str(int(numero)+1)
			num_constancia = str('GRC2014-'+str_number)
	    else:
	        num_constancia = 'GRC2014-1'
	    return num_constancia
	_defaults = {
	    'num_constancia' : _get_last_id
            }