from openerp.osv import osv, fields
class configuracionparroquia(osv.Model):
    _name = "configuracion.parroquia"
    _rec_name= "parroquia"
    #_order='parroquia'

   
      
    _columns = {
        'municipio_id' : fields.many2one('configuracion.municipio','Municipio', required=True , ondelete="cascade"),
        'parroquia' : fields.char(string="Parroquia",size=100, required=True),
    }