from openerp.osv import osv, fields
class configuracionmunicipio(osv.Model):
    _name = "configuracion.municipio"
    _rec_name="municipio"
    _order='municipio'

   
      
    _columns = {
        'municipio' : fields.char(string="Nombre",size=100, required=True),
        
    }