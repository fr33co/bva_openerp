# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class solicitud_modelo(osv.Model):
    _name = "solicitud.modelo"
    _order = 'modelo'
    _rec_name = 'modelo'
    
    _columns = {
        'modelo' : fields.char(string="Modelo", size=45, required=False),
        }
        
    _sql_constraints = [
        ('actividad_unique','UNIQUE(modelo)','El modelo debe ser unico.'),
        ]