from openerp.osv import osv, fields
class configuracionsector(osv.Model):
    _name = "configuracion.sector"
    _rec_name= "sector"
    _order='sector'

   
      
    _columns = {
        'municipio_id': fields.related('parroquia_id','municipio_id', type = 'many2one',relation = 'configuracion.municipio',string = 'municipio',required=True),
        'parroquia_id' : fields.many2one('configuracion.parroquia','Parroquia', required=True , ondelete="cascade"),
        'sector' : fields.char(string="Sector",size=100, required=True),
    }