from openerp.osv import osv, fields
class Gestiondocumentos(osv.Model):
    _name = "gestion.documentos"
   

   
      
    _columns = {
        'nrosolicitud_id' : fields.many2one('gestion.solicitudes','Numero de solicitud', required=True , ondelete="cascade"), 
        'fecha' : fields.date(string="Fecha de Emision",size=25, required=True),
        'documento' : fields.selection([('constancia','Constancia'),('certificacion','Certificacion'),('informe','Informe de Riesgo')],string="Documento a Generar",size=100, required=True),
        'descripcion' : fields.text(string="Descripcion",size=900, required=True),
        'funcionario_id' : fields.many2one('gestion.funcionarios','Funcionario Inspector', required=True , ondelete="cascade"),
        'num_documento' : fields.char(string="Numero de Documento",size=100,),
    }
    


    def get_last_id(self, cr, uid, ids, context = None):

        sfl_id  = self.pool.get('gestion.documentos')
        
        srchcnt_id = sfl_id.search_count(cr,uid,[])
        if srchcnt_id > 0:
            srch_id = sfl_id.search(cr,uid,[],offset=0,limit=1,order='num_documento desc')
            rd_id   = sfl_id.read(cr, uid, srch_id,['num_documento'], context=context)
            id_inspeccion = rd_id[0]['num_documento']
            numero = id_inspeccion[5]
            str_number = str(int(numero)+1)
            num_documento = str('GRSR-'+str_number)
        else:
            num_documento = 'GRSR-1'
        return num_documento
    _defaults = {
        'num_documento' : get_last_id
    }
