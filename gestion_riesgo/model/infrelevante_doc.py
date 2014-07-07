from openerp.osv import osv, fields
class infrelevantedoc(osv.Model):
	_name = "infrelevante.doc"
        
          
	_columns = {
	    'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"),
            'num_infrelevante' : fields.char(string="Numero de Informe Relevante",size=100,),
            'descripcion' : fields.text(string="Descripcion",size=900, required=True),
	}
        
        
        
        def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id  = self.pool.get('infrelevante.doc')
	    
	    srchcnt_id = sfl_id.search_count(cr,uid,[])
	    if srchcnt_id > 0:
			srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_infrelevante desc')
			rd_id   = sfl_id.read(cr, uid, srch_id,['num_infrelevante'], context=context)
			num_infrelevante = rd_id[0]['num_infrelevante']
			numero = num_infrelevante [10]
			str_number = str(int(numero)+1)
			num_infrelevante = str('GRIRE2014-'+str_number)
	    else:
	        num_infrelevante = 'GRIRE2014-1'
	    return num_infrelevante
	_defaults = {
	    'num_infrelevante' : _get_last_id
            }