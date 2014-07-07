# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv

class Becado(osv.Model):
	
	'''Herenciando a hr_employee (empleados)'''
	
	_order = "empleado"
	#~ _order = "tipo_beca asc"
	#~ _order = "entidad_bancaria asc"
	#~ _order = "status asc"
	
	_inherit = 'hr.employee'
	
	#------------------------------------------------------------------------------------------------------------------------------
	#Función para la generación del nombre completo del becado en base a los nombres y apellidos proporcionados en la ficha
	def constructor_name(self, cr, uid, ids, campo1, campo2, campo3, campo4, context=None):
		
		valores = {}
		
		#----------------------------------------
		if not campo1:
			nombre1 = ""
		else:
			nombre1 = str(campo1.encode("utf-8"))
		
		#----------------------------------------	
		if not campo2:
			nombre2 = ""
		else:
			nombre2 = str(campo2.encode("utf-8"))
			
		#----------------------------------------
		if not campo3:
			apellido1 = ""
		else:
			apellido1 = str(campo3.encode("utf-8"))
			
		#----------------------------------------
		if not campo4:
			apellido2 = ""
		else:
			apellido2 = str(campo4.encode("utf-8"))
			
		#----------------------------------------
		
		arreglo = []
		
		arreglo.append(nombre1)
		arreglo.append(nombre2) 
		arreglo.append(apellido1) 
		arreglo.append(apellido2)
		
		print arreglo
		
		nombre_completo = ""
		
		for nom_ape in arreglo:
			
			if nom_ape != 'False':
				
				nombre_completo += nom_ape+" "
				
		print nombre_completo
		
		
		valores.update({
			'name' : nombre_completo
		})
		
		return {'value':valores}
		
	#------------------------------------------------------------------------------------------------------------------------------
  #Funcion para calcular la edad del becado
	def validar_fecha(self, cr, uid, ids, fecha_nacimiento):

		values = {}

		edad = fecha_nacimiento

		edades = edad.split("-")

		fecha_actual = date.today()# Obtenemos el Ano actual der servidor

		ano_actual = fecha_actual.year # Segmentamos la fecha y obtenemos el ano actual

		mes_actual = fecha_actual.month

		dia_actual = mes_actual = fecha_actual.day


		calculo = int(ano_actual) - int(edades[0])


		values.update({

			'edad' : calculo,

			})
		return {'value' : values}
		
		
	#------------------------------------------------------------------------------------------------------------------------------
  #Funcion cargar un cero por defecto en el campo de número de cuenta si el personal a registrar tiene una categoría distinta de 'Becado'
	def carga_num_cuenta(self, cr, uid, ids, categoria):
		values = {}
		
		if categoria != "1":
			values.update({
				'numero_cuenta' : 'vacio',
				})
		
		return {'value' : values}
		
		
	#------------------------------------------------------------------------------------------------------------------------------
  #Funcion para cargar el id del banco por defecto
	def _banco_default(self, cr, user_id, context=None):

		cr.execute("SELECT id FROM becados_bancos WHERE banco = 'Venezuela'")
		id_banc = 0 # declaramos una tupla vacía
		for datos in cr.fetchall():
			id_banc = datos[0] #Id del banco
		return id_banc
		
	#-----------------------------------------------------------------------------------------------
	#~ Función para cargar datos de solicitantes seleccionados como posibles becados, utilizando
	#~ la cédula como clave de búsqueda.
	def datos_seleccionado(self, cr, uid, ids, cedula, context=None):
		valores = {}
		
		if not cedula:
			return valores
			
		#Preparación de los modelos donde se realizarán las búsquedas
		modelo1 = self.pool.get('becados.seleccion')
		modelo2 = self.pool.get('becados.solicitudes')
		
		#Ejecución de las búsquedas
		busqueda1 = modelo1.search_count(cr, uid, [('cedula','=',cedula)])
		
		if busqueda1 > 0:
			#Si se cumple esta condición es porque ha sido seleccionado, entonces procedemos 
			#a traer sus datos desde el otro modelo 
			busqueda2 = modelo2.search_count(cr, uid, [('cedula','=',cedula)])
			
			if busqueda2 > 0:
				busqueda2 = modelo2.search(cr, uid, [('cedula','=',cedula)])
				busqueda_leer = modelo2.read(cr, uid, busqueda2, context=context)
				
				#Carga de los datos que necesitamos
				valores.update({
					'name' : busqueda_leer[0]['solicitante'],
					'correo' : busqueda_leer[0]['email'],
					'tlf_local' : busqueda_leer[0]['telefono'],
					'tlf_movil' : busqueda_leer[0]['movil'],
					'grado_instruccion' : busqueda_leer[0]['grado_instruc'],
					'direccion' : busqueda_leer[0]['direccion'],
					'sede' : busqueda_leer[0]['sede'],
				})
				
				return {'value':valores}
	
	_columns = {
		#Información personal-----------------------------------------------------------------
		'cedula' : fields.char(string="Cédula", size = 10, required=True),
		'primer_nombre' : fields.char(string="Primer nombre", size=50, required=True),
		'segundo_nombre' : fields.char(string="Segundo nombre", size=50, required=False),
		'primer_apellido' : fields.char(string="Primer apellido", size=50, required=True),
		'segundo_apellido' : fields.char(string="Segundo apellido", size=50, required=False),
		'tiempo_servicio' : fields.char(string="Tiempo de Servicio", size = 50, required=False),
		'direccion' : fields.text(string="Dirección", size = 256, required=True),
		'correo' : fields.char(string="Correo", size = 30, required=False),
		'edad' : fields.char(string="Edad", size = 3, required=False),
		'camisa' : fields.char(string="Talla de Camisa", size=2, required=False),
		'pantalon' : fields.char(string="Talla de pantalón", size=2, required=False),
		'zapato' : fields.char(string="Calzado", size=2, required=False),
		'sexo' : fields.selection((('masculino','Masculino'),('femenino','Femenino')), "Sexo", required=False),
		'tlf_movil' : fields.char(string="Teléfono Movil", size = 11, required=True),
		'tlf_local' : fields.char(string="Teléfono Local", size = 11, required=False),
		'twitter' : fields.char(string="Twitter", size = 25, required=False),
		'cne' : fields.selection((('1','Si'),('2','No')), "¿Está inscrito en el CNE?", required = False),
		'centro_votacion' : fields.text(string="Centro de votación"),
		'discapacidad' : fields.selection((('1','Sí'),('2','No')),"¿Presenta discapacidad?",required=False),
		'tipo_discapacidad' : fields.selection((('1','Visual'),('2','Auditiva'),('3','Física'),('4','Psíquica'),('5','Multisensorial')),"Tipo de discapacidad",required=False),
		'carga_familiar' : fields.selection((('1','Dispone'),('2','No Dispone')), "¿Tiene Carga Familiar?", required = False),
		'carga_familiar2' : fields.selection((('1','Dispone'),('2','No Dispone')), "¿Tiene Carga Familiar?", required = False),
		'grupo_sanguineo': fields.many2one("becados.gruposanguineo", "Grupo Sanguineo", required = False),
		#Información académica----------------------------------------------------------------
		'grado_instruccion': fields.many2one("becados.gradoinstruccion", "Grado de Instrucción", required = True),
		'nivel_edu' : fields.many2one("becados.niveleduc","Nivel Educativo",required=False),
		'titulo_obtenido' : fields.char(string="Título Obtenido", size = 11, required=False),
		'estado_de_estudios' : fields.boolean("¿Estudia Actualmente?"),
		'inst_educ' : fields.many2one("becados.institucioneduc","Institución",required=False),
		'estudios_actuales' : fields.char(string="Especifique qué estudia",required=False),
		#Información institucional------------------------------------------------------------
		'fecha_ingreso' : fields.date(string="Fecha de Ingreso", required=True),
		'fecha_egreso' : fields.date(string="Fecha de Egreso", required=False),
		'tipo_nomina' : fields.many2one("becados.tiponomina", "Tipo de Nómina", required = False),
		'class_personal' : fields.many2one("becados.clasper", "Clasificación del Personal", required = False),
		'empleado': fields.many2one("becados.tipoempleado", "Tipo de Empleado", required = False),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required = False),
		'area' : fields.many2one("becados.areas", string="Area de desempeño", required=False),
		'ejes' : fields.many2one("becados.ejes", "Eje", required = False), #Inhabilitado
		'eje' : fields.selection((('001','Eje Centro'),('002','Eje Costa'),('003','Eje Este'),('004','Eje Metro'),('005','Eje Sur')),"Eje",required=True),
		'sede' : fields.many2one("becados.sedes", "Sede/Unidad Asignada", required=False),
		'cargo_desempenado' : fields.selection((('1','0243'),('2','0244')), "Cargo Desempeñado", required = False),
		'coordinador_eje' : fields.many2one("hr.employee","Coordinador de Eje",required=False, domain=[('categoria','=','4')]),
		'coordinador_sede' : fields.many2one("hr.employee","Coordinador de Sede",required=False, domain=[('categoria','=','5')]),
		#'status' : fields.many2one("becados.status","Status",required=False),
		'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
		'desc_status' : fields.char(string="Descripción", size=100, required=False,help="Escriba aquí detalles y razones del estatus seleccionado"),
		'asignacion' : fields.float(string="Asignación", required=False),
		'entidad_bancaria' : fields.many2one("becados.bancos", "Entidad Bancaria", required = True),
		'numero_cuenta' : fields.char(string="Número de cuenta",size=20,required=True),
		'tipo_cuenta' : fields.selection((('0','Corriente'),('1','Ahorro')),"Tipo de Cuenta",required=True),
		'ano_antiguedad' : fields.char(string="Año de Antiguedad", required=False),
		'caja_ahorro' : fields.char(string="Caja de Ahorro", required=False),
		#~ 'prima_responsabilidad' : fields.float(string="Prima de Responsabilidad", required=False),
		'prima_responsabilidad' : fields.selection((('1','Si'),('2','No')),"Prima responsabilidad",required=False),
		#'fecha_nacimiento' : fields.date(string="Fecha de nacimiento", required=True),
		'familiar' : fields.one2many("becado.carga.familiar","becado",string="Carga Familiar"),
		'categoria' : fields.selection((('1','Becado'),('2','Empleado'),('3','Obrero'),('4','Coordinador_eje'),('5','Coordinador_sede')), "Categoria", required = True),
		#Información de representante/contacto------------------------------------------------
		'cedula_contacto' : fields.integer(string="Cédula",size=8,required=False),
		'nombre_contacto' : fields.char(string="Nombre y Apellido",required=False),
		'direccion_contacto' : fields.text(string="Dirección",size=256,required=False), 
		'telefono_contacto' : fields.char(string="Teléfono",size=12,required=False),
		'correo_contacto' : fields.char(string="Correo",size=50,required=False),
		'contacto' : fields.one2many("becados.contactos","becado",string="Contactos",required=False),
		#Campos extra-------------------------------------------------------------------------
		'fecha_actual' : fields.char(string="FECHA", size = 50, required=False),#Campo para formato PDF
		'grupo' : fields.many2one("res.groups", "Grupos", required=True, readonly=True),	
	}
	
	_defaults = {
		'fecha_actual': lambda *a: time.strftime("(%d) días del mes %B del año %Y"),# formato corecto al español
		'status' : '1',
		'grupo': lambda s, cr, uid, c: uid,
		'tipo_cuenta' : '0',
		'entidad_bancaria' : _banco_default,
		'eje' : "001",
		#~ 'categoria' : '1',
		#~ 'tipo_beca' : '1',
		#~ 'entidad_bancaria' : '1',
		#~ 'tipo_cuenta' : '1'
	}
	
	#------------------------------------------------------------------------------------------------------------------------------
  #Funcion validar que la longitud del campo de número de cuenta sea igual a 20 dígitos
	#~ def validar_num_cuenta(self, cr, uid, ids, num_cuenta, context=None):
		#~ values = {}
		#~ mensaje = {}
		#~ b = ""
		#~ b2 = ""
		#~ b3 = ""
		#~ 
		#~ if not num_cuenta:
			#~ return values
		#~ 
		#~ for reg in self.browse(cr, uid, ids, context=context):
			#~ b = reg.entidad_bancaria
			#~ b2 = reg.entidad_bancaria.id
			#~ b3 = reg.entidad_bancaria.banco
		#~ 
		#~ print "id del banco: "+str(b)
		#~ print "id del banco: "+str(b2)
		#~ print "nombre del banco: "+str(b3)
			
		#~ if b == "Venezuela":
			#~ n = str(num_cuenta)
			#~ print len(n)
			#~ print b
			#~ 
			#~ if len(n) < 20:
				#~ mensaje = {
					#~ 'title'   : "Número de cuenta",
					#~ 'message' : "Disculpe el número de cuenta debe contener un mínimo de 20 dígitos... "+b,
				#~ }
				#~ values.update({
					#~ 'numero_cuenta' : None,
				#~ })
		
		#~ return True
		#~ return {'value' : values, 'warning' : mensaje} 
