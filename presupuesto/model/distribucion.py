from openerp.osv import osv, fields
import random
import time
from datetime import datetime, timedelta
class Distribucion(osv.Model):
    _name = "presupuesto.distribucion"



    _columns = {
        'proyecto': fields.related('accion','proyecto', type = 'many2one',relation = 'presupuesto.proyecto',string = 'Proyecto',required=True,),
        'codigo_accion' : fields.char(string="Codigo del Accion",size=11,readonly=False),
        'accion' : fields.many2one('presupuesto.accion','Accion',ondelete='cascade',required=True),
        'partida' : fields.char(string="Partida Presupuestaria",size=12, required=True),
        'descripcion' : fields.char(string="Partida",size=300, required=True),
        'monto_pre' : fields.float(string="Monto del Presupuesto",size=12, required=True),
        'aceptar' : fields.selection((('1','Ambos'), ('2','Compras'), ('3', 'Servicios')),'Aceptar orden de', required=True),
        'fecha' : fields.date(string="Fecha Apertura", required=True),
        'disponibilidad' : fields.float(string="Disponibilidad Actual",readonly=False),
        'monto_proyecto' : fields.float(string="Monto del Proyecto",readonly=False),
        'incidencias_ids': fields.one2many('presupuesto.accion', 'distribucion_id', string="Incidencias"),
    }

    _defaults = {
        'proyecto':lambda *a: 0,
    }
    def on_change_accion(self, cr, uid, ids, accion,context=None):
        values = {}
        if not accion:
            return values
        obj_accion    = self.pool.get('presupuesto.accion').browse(cr, uid, accion, context=context)
        obj_proyecto  = self.pool.get('presupuesto.proyecto')
        srch_proyecto = obj_proyecto.search(cr, uid, [('id','=', obj_accion.id)])
        rd_proyecto   = obj_proyecto.read(cr, uid, srch_proyecto, context=context)

        values.update({'codigo_accion' : obj_accion.codigo_accion,'disponibilidad' : obj_accion.monto,'monto_proyecto':rd_proyecto[0]['monto']})

        return {'value' : values}

    def on_change_partida(self, cr, uid, ids, partida, context=None):
        values = {}
        if not partida:
            return values
        obj_partida  = self.pool.get('presupuesto.partidas')
        srch_partida =  obj_partida.search(cr, uid, [('codigo','=', partida)])
        rd_partida   = obj_partida.read(cr, uid, srch_partida, context=context)
        descripcion  = rd_partida[0]['descripcion']
        values.update({'descripcion' : descripcion,})
        return {'value' : values}

    def on_change_disminuirmonto(self, cr, uid, ids, partida, context=None):
        values = {}
        if not partida:
            return values
        obj_partida  = self.pool.get('presupuesto.partidas')
        srch_partida =  obj_partida.search(cr, uid, [('codigo','=', partida)])
        rd_partida   = obj_partida.read(cr, uid, srch_partida, context=context)
        descripcion  = rd_partida[0]['descripcion']
        values.update({
                'descripcion' : descripcion,
        })
        return {'value' : values}
    _order='codigo_accion'
    _rec_name='descripcion'

