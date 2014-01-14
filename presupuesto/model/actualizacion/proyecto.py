#-*- coding:utf-8 -*-
###########################################################
#
# Clase para crear el proyecto del modulo de presupuesto
#
###########################################################
from openerp.osv import osv, fields
import random

class Proyecto(osv.Model):
    """
     Crear el objeto 'presupuesto.proyecto'
    """
    _name = "presupuesto.proyecto"

    """
        Declaracion de las Columnas para el xmly la base de datos
    """
    _columns = {
        'codigo_proyecto' : fields.char(string="Codigo del Proyecto:",size=100, required=True,help="Prueba"),
        'proyecto' : fields.char(string="Nombre del Proyecto:",size=100, required=True),
        'monto' : fields.float(string="Montos:",size=100, required=True),
        'descripcion' : fields.text(string="Descripcion:",size=300, required=True),
    }

    """
        Ordenar por proyecto y llamar el nombre del proyecto
    """
    _order='proyecto'
    _rec_name='proyecto'

