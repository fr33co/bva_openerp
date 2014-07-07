{
    'name' : "Desarrollo Social",
    'category' : "Desarrollo Social",
    'version' : "1.0",
    'depends' : ['base','hr','hr_payroll','hr_recruitment','hr_contract','l10n_ve_topology'],
    'author' : "Departamento de Desarrollo y Aplicaciones",
    'description' : '''\
     El modulo de Desarrollo Social permite el manejo y gestion de los becados de las diferentes Bibliotecas Virtuales de Aragua:
			Registro
      Edicion
      Generación de Reportes
			Generación de Nóminas
		 Depende del módulo de Recursos Humanos desarrollado en el departamento y del modelo hr.employee''',
    'data' : [
      "views/becado.xml",
      "views/nomina.xml", # nómina
      "views/proceso_nomina.xml", # Procesos de nóminas
      "views/tipoNomina.xml",
      "views/carga_familiar.xml",
      "views/clasPer.xml",
      "views/tipoEmp.xml",
      "views/gradoInstruccion.xml",
      "views/grupoSanguineo.xml",
      "views/sedes.xml",
      "views/areas.xml",
      "views/tipo_beca.xml",
      "views/status.xml",
      "views/novedades.xml",
      "views/proceso_seleccion.xml",
      "views/seleccion.xml",
      "views/solicitudes.xml",
      "views/contrato.xml",
      "views/evaluacion.xml",
      "views/nivel_edu.xml",
      "views/ejes.xml",
      "views/institucion_edu.xml",
      "views/banco.xml",
      "views/contacto.xml",
      "views/nomina_becados.xml",
      "views/nomina_becado_individual.xml",
      "views/archivos_nominas.xml",
      "views/wizard_lista_becados/wizard_lista_becados.xml",
      "views/calculo_nomina.xml",
      #"reportes/report_becados.xml",
      "categorias/mantenimiento.xml",
      "seguridad/groups.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      #""seguridad/users.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
      "seguridad/ir.model.access.csv",
      #"categorias/categorias.xml", #Activar la carga de este archivo sólo al instalar, luego comentarlo.
			"reportes/evaluacion/report_evaluacion.xml", # Reporte para casos de novedad del becado
      "reportes/novedad/report_becados.xml", # Reporte para casos de novedad del becado
      "reportes/constancia/constancia.xml", # Reporte para la emisión de constancia
    ],
    'css': [ 'static/src/css/style.css' ],
}
