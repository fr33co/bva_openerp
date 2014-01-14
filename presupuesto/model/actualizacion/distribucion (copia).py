from openerp.osv import osv, fields
import random
import time
from datetime import datetime, timedelta
class Distribucion(osv.Model):
    _name = "presupuesto.distribucion"

    _columns = {
        'proyecto_id': fields.related('accion','proyecto_id', type = 'many2one',relation = 'presupuesto.proyecto',string = 'Proyecto',required=True,),
        'codigo_accion' : fields.char(string="Codigo del Accion",size=11,required=True),
        'accion' : fields.many2one('presupuesto.accion','Accion',ondelete='cascade',required=True),
        'partida' : fields.char(string="Partida Presupuestaria",size=12, required=True),
        'descripcion' : fields.many2one('presupuesto.partidas','Partidad',ondelete='cascade',required=True),
        'monto_pre' : fields.float(string="Monto del Presupuesto",size=12, required=True),
        'aceptar' : fields.selection((('1','Ambos'), ('2','Compras'), ('3', 'Servicios')),'Aceptar orden de'),
        'fecha' : fields.date(string="Fecha Apertura", required=True),
        'disponibilidad' : fields.float(string="Disponibilidad Actual",readonly=False),
        'monto_proyecto' : fields.float(string="Monto del Proyecto",readonly=False),
    }


    def on_change_accion(self, cr, uid, ids, accion,tipo,context=None):
        values = {}
        if not accion:
            return values

        id_accion = 0
        obj_accion    = self.pool.get('presupuesto.accion')
       
        if tipo == 'cod_accion':
            srch_accion = obj_accion.search(cr, uid, [('codigo_accion','=', accion)])
            rd_accion   = obj_accion.read(cr, uid, srch_accion, context=context)
            if rd_accion != False:
                id_accion  = rd_accion[0]['id']
                values.update({'accion' : id_accion})
        else:
            brw_accion  = obj_accion.browse(cr, uid, accion, context=context)
            if brw_accion != False:

                id_accion        = brw_accion.codigo_accion
                values.update({'codigo_accion' : id_accion})

            monto_disponible = brw_accion.monto
            id_proyecto      = brw_accion.proyecto_id

            obj_proyecto   = self.pool.get('presupuesto.proyecto')
            srch_proyecto  = obj_proyecto.search(cr, uid, [('id','=',id_proyecto.id)])
            rd_proyecto    = obj_proyecto.read(cr, uid, srch_proyecto, context=context)
            monto_proyecto = rd_proyecto[0]['monto']
            values.update({'disponibilidad' : monto_disponible,'monto_proyecto':monto_proyecto})
        return {'value' : values}

    def on_change_partida(self, cr, uid, ids, partida,tipo='select', context=None):

        values = {}
        if not partida:
            return values

        obj_partida  = self.pool.get('presupuesto.partidas')
        if tipo == 'cod_partida':
            srch_partida =  obj_partida.search(cr, uid, [('codigo','=', partida)])
            rd_partida   = obj_partida.read(cr, uid, srch_partida, context=context)
            if not rd_partida:
                id_part = 0
            else:
                id_part  = rd_partida[0]['id']
            values.update({'descripcion' : id_part})
        else:
            srch_partida =  obj_partida.search(cr, uid, [('id','=', partida)])
            rd_partida   = obj_partida.read(cr, uid, srch_partida, context=context)
            if not rd_partida:
                descripcion = None
            else:
                descripcion  = rd_partida[0]['codigo']
            values.update({'partida' : descripcion})

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

