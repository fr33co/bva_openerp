{
    'name' : "Gestión de Eventos",
    'category' : "Gestión de Eventos",
    'version' : "1.4",
    'depends' : ['base','l10n_ve_topology'],
    'author' : "Ing en Sistemas: Jesús G. Laya R",
    'description' : '''
     El módulo de Gestión de Eventos, permite la Gestión de Eventos para la Gobernación del Estado Aragua
      Edicion
      Gestión de Eventos
      Ultima Actualización: 04 de Julio del 2014''',
    'data' : [
      "views/gestion_eventos.xml", # Gestion de eventos
      "views/institucion_gerencia.xml", # Institucion / Gerencia
      "views/gestion_documento.xml", # Gestion de Documentos
      "views/recurso_logistico.xml",
      "views/usuario_gerencia.xml", # Usuario por Gerencia
      "views/gestion_reportes.xml", # Gestion de Reportes
      "script/script.xml", # Script de carga de data
      "foto/foto.xml",
    ],
    'css': [ 'static/src/css/style.css' ],
}
