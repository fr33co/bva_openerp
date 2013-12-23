from openerp.osv import osv, fields
from openerp.tools.translate import _
class Accion(osv.Model):
    _name = "presupuesto.accion"



    _columns = {
    'proyecto' : fields.many2one('presupuesto.proyecto','Proyecto',ondelete='cascade',required=True),
    'distribucion_id' :fields.many2one('presupuesto.distribucion','Proyecto',ondelete='cascade',required=True),
    #'codigo_proyecto' : fields.char(string="Codigo del Proyecto",size=100, readonly=True),
    'codigo_accion' : fields.char(string="Codigo de Accion",size=11, required=True),
    #'codigo_a_p' : fields.char(string="Codigo",size=10, required=True),
    'siglas' : fields.char(string="Siglas",size=300, required=True),
    'descripcion' : fields.text(string="Descripcion",size=300, required=True),
    'unidad' : fields.char(string="Unidad Ejecutora",size=100, required=True),
    'monto' : fields.float(string="Monto",size=100, required=True),
    }

    def on_change_proyecto(self, cr, uid, ids, proyecto, context=None):
        #raise osv.except_osv(('VENTANA DE ERROR'), ('ocurrio un Error' ) )


        values = {}
        if not proyecto:
            return values
        proyecto = self.pool.get('presupuesto.proyecto').browse(cr, uid, proyecto, context=context)
        values.update({'codigo_accion' : proyecto.codigo_proyecto+'-',})
        return {'value' : values}

    def on_change_cod_accion(self, cr, uid, ids, valor, context=None):
        print valor
        #values = {}
        #if not proyecto:
        #    return values
        self.write(cr, uid, ids, {'codigo_a_p': valor}, context)
        values.update({
               'codigo_a_p' : proyecto
        })
        #return {'value' : values}
    _order='codigo_accion'
    _rec_name='descripcion'

