from openerp.osv import osv, fields
import random
class CreditosAdiconales(osv.Model):
    _name = "presupuesto.creditos"



    _columns = {
        'id_tipo_doc' : fields.char(string="Tipo de Documento",size=100, required=True),
        'numero' : fields.char(string="Numero:",size=100, required=True),
        'fecha' : fields.date(string="Fecha:", required=True),
        'oficio' : fields.char(string="# Oficio:", required=True),
        'fecha_oficion' : fields.date(string="Fecha de Oficio:", required=True),
        'observacion' : fields.char(string="Motivo:", required=True),
        'proyecto_accion' : fields.char(string="Proyecto Accion",size=100, required=True),
        'cosulta_proyecto_accion' : fields.char(string="Consulta de Proyecto Accion:",size=100, required=True),
        'cod_presupuesto' : fields.char(string="Cod Presupuestario",size=100, required=True),
        'desc_presupuesto' : fields.char(string="Desc Presupuesto:",size=100, required=True),
    }


    _order='id_tipo_doc'
    _rec_name='id_tipo_doc'

