# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Contacto(osv.Model):
	_name="becados.contactos"

	_order = 'cedula_contacto'
	
	_rec_name = 'cedula_contacto'
	
	_columns = {
		'becado' : fields.many2one("hr.employee","Becado",required=False,domain=[('categoria','=','1')]),
		'cedula_contacto' : fields.integer(string="Cédula",size=8,required=False),
		'nombre_contacto' : fields.char(string="Nombre y Apellido",required=False),
		'direccion_contacto' : fields.text(string="Dirección",size=256,required=False), 
		'telefono_contacto' : fields.char(string="Teléfono",size=12,required=False),
		'correo_contacto' : fields.char(string="Correo",size=50,required=False),
		'parentesco' : fields.selection((('1','Hijo(a)'),('2','Madre'),('3','Padre'),('4','Esposo(a)'),('5','Unión Estable')), "Parentesco", required = False),
	}
