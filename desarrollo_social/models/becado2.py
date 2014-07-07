# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from openerp.osv import osv, fields

class Becado(osv.Model):
	_name = "becados"
	
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result
    
	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'foto': tools.image_resize_image_big(value)}, context=context)
	
	_columns ={
		#Sección I (Datos Personales)
		'cedula': fields.char(string = "Cédula", size = 9, required = True),
		'nombres': fields.char(string = "Nombres", size = 30, required = True),
		'apellidos': fields.char(string = "Apellidos", size = 30, required = True),
		'sexo': fields.selection((('1','Masculino'),('0','Femenino')), "Sexo", required = True),
		'fecha_nac': fields.date(string = "Fecha de Nacimiento", required = True),
		'lugar_nac': fields.text(string = "Lugar de Nacimiento", size = 256, required = True),
		'estado_civil': fields.selection((('1','Soltero'),('2','Casado'),('3','Divorciado'),('4','Viudo'),('2','Conyugue')), "Estado Civil", required = True),
		'direccion' : fields.text(string = "Dirección", size = 256, required = True),
		'cod_tel_movil': fields.selection((('1','0416'),('2','0412')), "Código", required = True),
		'tel_movil': fields.char(string="Teléfono Móvil", size = 12, required = True),
		'cod_tel_fijo': fields.selection((('1','0243'),('2','0244')), "Código", required = True),
		'tel_fijo': fields.char(string="Teléfono Fijo", size = 12, required = True),
		'correo': fields.char(string = "Correo", size = 50, required = True),
		'twitter': fields.char(string = "Twitter", size = 25, required = False),
		'grado_instruc': fields.selection((('1','Primaria'),('2','Bachiller'),('3','Técnico Superior Universitario'),('4','Universitario'),('2','Postgrado')), "Grado de Instrucción", required = True),
		'titulo_obt': fields.char(string = "Título Obtenido", size = 30, required = False),
		'grupo_sangre': fields.selection((('1','O+'),('2','O-')), "Grupo Sanguineo", required = False),
		'tipo_emp': fields.selection((('1','Cyber Guía 1'),('2','Cyber Guía 2')), "Tipo de Empleado", required = True),
		'estatus': fields.selection((('1','Activo'),('2','Suspendido'),('3','Egresado')), "Estatus", required = True),
		'tiempo_serv': fields.char(string = "Tiempo de Servicio", size = 9, required = True),
		'foto': fields.binary("Foto", required = False, help="Subir Foto"),
		'num_historial' : fields.char(string = "Número de Historial", size = 9, required = False),
		#Sección II (Becado/Empresa)
		'fecha_ing' : fields.date(string = "Fecha de Ingreso", required = True),
		'fecha_egre' : fields.date(string = "Fecha de Egreso", required = False),
		'tipo_nomina' : fields.selection((('1','BECADO BBVVA'),('2','BECADO BBVVA 2')), "Tipo de Nómina", required = False),
		'class_personal' : fields.selection((('1','CYBERGUIA 1'),('2','CYBERGUIA 2')), "Clasificación del Becado", required = False),
		'cargo': fields.selection((('1','Becado 1'),('2','Becado 2')), "Cargo", required = True),
		'departamento': fields.selection((('1','Biblioteca Virtual Barrio del Carmen'),('2','Biblioteca Virtual Francisco de Miranda')), "Departamento", required = True),
		'sueldo' : fields.float(string="Sueldo", required=True),
		'numero_cuenta': fields.char(string = "Número de Cuenta", size = 30, required = True),
		'tipo_banco': fields.selection((('1','Cuenta de Ahorro'),('2','Cuenta Corriente')), "Cuenta Bancaria", required = True),
		'ano_ant' : fields.char(string="Año de Antigüedad", required=True),
		'Camisa' : fields.char(string="Camisa", required=False),
		'pantalon' : fields.char(string="Pantalón", required=False),
		'zapato' : fields.char(string="Zapato", required=False),
		'caja_ahorro' : fields.float(string="Caja de Ahorro", required=False),
		'prima_resp' : fields.float(string="Prima de Responsabilidad", required=False),
		
	}
