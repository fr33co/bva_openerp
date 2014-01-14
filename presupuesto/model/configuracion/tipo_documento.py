from openerp.osv import osv, fields
import random
class Documento(osv.Model):
    _name = "presupuesto.documento"

    _order='id_documento desc'
    _rec_name='documento'

    _columns = {
        'id_documento' : fields.char(string="Codigo del Documento:",size=100),
        'siglas' : fields.char(string="Siglas del Documento:",size=6, required=True),
        'documento' : fields.char(string="Tipo de Documento:",size=100, required=True),
        'tipo' : fields.selection((('1','Traspaso/Traslado'), ('2','Creditos Adiconales')),'Tipo', required=True),
    }

    def _get_last_id(self, cr, uid, ids, context = None):

        sfl_id       = self.pool.get('presupuesto.documento')
        srch_id      = sfl_id.search(cr,uid,[],offset=0,limit=1,order='id_documento desc',count=True)
        rd_id        = sfl_id.read(cr, uid, srch_id,['id_documento'], context=context)
        
        if rd_id:
            id_documento = rd_id['id_documento']
            last_id      = id_documento.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(6,'0')
        else :
            str_number = '1'
            last_id    = str_number.rjust(6,'0')
        return last_id
    _defaults = {
        'id_documento' : _get_last_id
    }