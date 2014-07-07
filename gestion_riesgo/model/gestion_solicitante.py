from openerp.osv import osv, fields
class Gestionsolicitante(osv.Model):
    _name = "gestion.solicitante"
   

   
      
    _columns = {
        'cedula' : fields.integer(string="Cedula",size=25, required=True),
        'nombre' : fields.char(string="Nombres",size=100, required=True),
        'apellido' : fields.char(string="Apellidos",size=100, required=True),
        'fecha' : fields.date(string="Fecha de Nacimiento",size=100, required=True),
        'movil' : fields.char(string="Telefono Movil",size=11,),
        'fijo' : fields.char(string="Telefono Fijo",size=11,),
        'municipio_id': fields.related('parroquia_id','municipio_id', type = 'many2one',relation = 'configuracion.municipio',string = 'Municipio',required=True),
        'parroquia_id': fields.related('sector_id','parroquia_id', type = 'many2one',relation = 'configuracion.parroquia',string = 'Parroquia',required=True),
        'sector_id' : fields.many2one('configuracion.sector','Sector', required=True , ondelete="cascade"),
        'direccion' : fields.text(string="Direccion",size=300, required=True),
        'email' : fields.char(string="Email",size=100,),
        'funcionario' : fields.selection([('si','Si'),('no','No'),],string="Funcionario PCADA",size=100, required=True),
        'cargo' : fields.char(string="Cargo",size=100),
    }