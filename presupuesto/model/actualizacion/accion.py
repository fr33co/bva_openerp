#-*- coding:utf-8 -*-
###############################################################################################
#
# Clase para crear las acciones presupuestarias dependientes del proyecto del modulo de presupuesto 
#
###############################################################################################
from openerp.osv import osv, fields
class Accion(osv.Model):

    """
     Crear el objeto 'presupuesto.accion'
    """
    _name = "presupuesto.accion"

    """
        Declaracion de las Columnas para el xmly la base de datos
    """

    _columns = {
    # Campo que genera una lista desplegable del los proyectos generados en el modulo de proyecto
    'proyecto_id' : fields.many2one('presupuesto.proyecto','Proyecto',ondelete='cascade',required=True), 
    'codigo_accion' : fields.char(string="Codigo de Accion",size=11, required=True),
    'siglas' : fields.char(string="Siglas",size=300, required=True),
    'descripcion' : fields.text(string="Descripcion",size=300, required=True),
    'unidad' : fields.char(string="Unidad Ejecutora",size=100, required=True),
    'monto' : fields.float(string="Monto",size=100, required=True),
    }

    """
    Metodo para buscar el codigo del proyecto seleccionado en el combo list,
    y asi generar el codigo de la accion
    """

    def on_change_proyecto(self, cr, uid, ids, proyecto, context=None):
        values = {}
        if not proyecto:
            return values
        sls_cod_proyect = self.pool.get('presupuesto.proyecto')
        brw_cod_proyect = sls_cod_proyect.browse(cr, uid,proyecto, context=context)
        values.update({'codigo_accion' : brw_cod_proyect.codigo_proyecto+'-',})

        return {'value' : values}

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order='codigo_accion'
    _rec_name='descripcion'

