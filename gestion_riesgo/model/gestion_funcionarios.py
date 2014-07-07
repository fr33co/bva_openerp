from openerp.osv import osv, fields
class Gestionfuncionarios(osv.Model):
    _name = "gestion.funcionarios"
    _rec_name = "union"
   

   
      
    _columns = {
        'nombre' : fields.char(string="Nombre del Funcionario",size=100, required=True),
        'apellido' : fields.char(string="Apellido del Funcionario",size=100, required=True),
        'cedula' : fields.integer(string="Cedula",size=25, required=True),
        'cargo' : fields.char(string="Cargo",size=100, required=True),
        'union' : fields.char(string="Funcionario", size=100,)
    }



    def concatenar(self, cr, uid, ids, nombre, apellido, context = None):
	    
		values = {}
		if not apellido:
			return values

		union_id = str(nombre)+' '+str(apellido) 

		values.update({'union' : union_id,})
		return {'value' : values} 
	