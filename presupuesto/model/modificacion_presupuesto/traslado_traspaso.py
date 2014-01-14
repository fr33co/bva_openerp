from openerp.osv import osv, fields
import random
class Traslado(osv.Model):
    _name = "presupuesto.traslado"

    _order    ='tipo_doc'
    _rec_name ='tipo_doc'

    _columns = {
        'tipo_doc' : fields.many2one('presupuesto.documento','Tipo Doc',ondelete='cascade',required=True,domain=[('tipo', '=', '1')]),
        'numero' : fields.char(string="Numero:",size=100, required=True),
        'fecha' : fields.date(string="Fecha:", required=True),
        'oficio' : fields.char(string="# Oficio:", required=True),
        'fecha_resolucion' : fields.date(string="Fecha de Resolucion:", required=True),
        'motivo' : fields.char(string="Motivo:", required=True),
        'categoria' : fields.char(string="Categoria:", required=True),
        'consulta_categoria' : fields.many2one('presupuesto.accion','Consulta de Categoria:',ondelete='cascade',required=True),
        'cod_presupuesto' : fields.char(string="Cod Presupuestario:", required=True),
        'par_presu' : fields.char(string="Cod Presupuesto:",readonly=True),
        'monto_movi' : fields.float(string="Monto Movimiento:", required=True),
        'monto_movi1' : fields.float(string="Monto Movimiento:"),
        'aumen_dism': fields.selection([('aumento','Aumentar'),('disminuye','Disminuir')],'Aumentar/Disminuir'),
        'aumentar' : fields.float(string="Aumentar:",),
        'disminuir' : fields.float(string="Disminuir:",),
        'disponibilidad' : fields.char(string="Disponibilidad:"),
    }

    def get_last_numero(self, cr, uid, ids, tipo_doc, context = None):
        values = {}
        vlores = {}
        if not tipo_doc:
            return values

        sfl_last_num   = self.pool.get('presupuesto.traslado')
        srch_last_num  = sfl_last_num.search(cr,uid,[('tipo_doc','=',tipo_doc)],offset=0,limit=1,order='numero desc',count=True)
        rd_last_num    = sfl_last_num.read(cr, uid, srch_last_num,['numero'],context=context)

        if not rd_last_num:
            str_number = '1'
            last_num   = str_number.rjust(7,'0')
        else :
            last_num   = rd_last_num['numero']
            last_num   = last_num.lstrip('0')
            str_number = str(int(last_num) + 1)
            last_num   = str_number.rjust(7,'0')

        valores = {'numero' : last_num}

        values.update(valores)

        return {'value' : values}

    def on_change_accion(self, cr, uid, ids, accion,tipo,context=None):
        values    = {}
        valores   = {}
        id_accion = 0
        if not accion:
            return values

        sfl_accion = self.pool.get('presupuesto.accion')

        if tipo == 'cod_accion':

            srcnt_accion = sfl_accion.search_count(cr, uid, [('codigo_accion','=', accion)], context=None)
            if srcnt_accion  > 0:
                srch_accion = sfl_accion.search(cr, uid, [('codigo_accion','=', accion)])
                rd_accion   = sfl_accion.read(cr, uid, srch_accion, context=context)
                id_accion   = rd_accion[0]['id']

            valores   = {'consulta_categoria' : id_accion}
        else:
            brw_accion  = sfl_accion.browse(cr, uid, accion, context=context)
            if brw_accion != False:
                id_accion = brw_accion.codigo_accion
            valores   = {'categoria' : id_accion}

        values.update(valores)
        return {'value' : values}


    def on_change_partida(self, cr, uid, ids, partida, context=None):
        valores = {}
        values  = {}
        id_part = 0
        if not partida:
            return values

        sfl_partida   = self.pool.get('presupuesto.partidas')
        srcnt_partida = sfl_partida.search_count(cr, uid, [('codigo','=', partida)], context=None)

        if srcnt_partida > 0:
            srch_partida = sfl_partida.search(cr, uid, [('codigo','=', partida)])
            rd_partida   = sfl_partida.read(cr, uid, srch_partida, context=context)
            id_part      = rd_partida[0]['descripcion']

        valores = {'par_presu' : id_part}
        values.update(valores)
        return {'value' : values}

    def on_change_montomovi(self, cr, uid, ids, monto, context=None):
        values = {}
        valores = {'monto_movi1' : monto}
        values.update(valores)
        return {'value' : values}

    def on_change_get_row(self, cr, uid, ids, numero,tipo_doc, context=None):
        values  = {}
        valores = {}

        valores = {
                                'fecha': None,
                                'oficio': None,
                                'fecha_resolucion':None,
                                'motivo': None,
                                'categoria': None,
                                'consulta_categoria': 0,
                                'monto_movi': 0.00,
                                'aumen_dism': None,
                            }

        if not numero:
            return values

        sfl_get_row    = self.pool.get('presupuesto.traslado')

        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('tipo_doc','=',tipo_doc),('numero','=',numero)], context=None)

        if srcnt_get_row > 0:
            srch_get_row = sfl_get_row.search(cr,uid,[('tipo_doc','=',tipo_doc),('numero','=',numero)])
            rd_get_row    = sfl_get_row.read(cr, uid, srch_get_row,context=context)
            valores = {
                                'fecha': rd_get_row[0]['fecha'],
                                'oficio': rd_get_row[0]['oficio'],
                                'fecha_resolucion': rd_get_row[0]['fecha_resolucion'],
                                'motivo': rd_get_row[0]['motivo'],
                                'categoria': rd_get_row[0]['categoria'],
                                'cod_presupuesto': rd_get_row[0]['cod_presupuesto'],
                                'monto_movi': rd_get_row[0]['monto_movi'],
                                'aumen_dism': rd_get_row[0]['aumen_dism'],
                            }

        values.update(valores)
        return {'value' : values}

