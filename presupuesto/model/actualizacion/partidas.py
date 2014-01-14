#-*- coding:utf-8 -*-
###############################################################################################
#
# Clase para crear las partidas presupuestarias  del modulo de presupuesto 
#
###############################################################################################
from openerp.osv import osv, fields
import random
class Partidas(osv.Model):

    """
     Crear el objeto 'presupuesto.accion'
    """
    _name = "presupuesto.partidas"


    """
        Declaracion de las Columnas para el xmly la base de datos
    """
    _columns = {
        # many2one para llamar el mismo combo list de esta clase  
        'id_partida' : fields.many2one('presupuesto.partidas','Padre:',ondelete='cascade'),
        'codigo' : fields.char(string="Codigo:",size=20, required=True),
        'descripcion' : fields.text(string="Descripcion:",size=300, required=True),

    }

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order='codigo'
    _rec_name='descripcion'

