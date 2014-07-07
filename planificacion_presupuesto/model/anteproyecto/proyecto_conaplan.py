# -*- coding: utf-8 -*-
import hashlib
import itertools
import logging
import os
import re
import class_pdf
import base64
import random
import unicodedata
from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
import xlwt
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
import re
import unicodedata
import base64 #Necesario para la generación del .xls

# Clase Solicitud de reparacion de Canaima
class solicitud_soporte(osv.Model):

    #  Nombre del objeto
    _name = "proyecto.conaplan"

    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'


    """
    Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
    y se le suma 1.
    """
    def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id       = self.pool.get('proyecto.conaplan')
	    srch_id      = sfl_id.search(cr,uid,[])
	    rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
	    if rd_id:
		id_documento = rd_id[-1]['c_solicitud']
		c_nota = id_documento[:]
		last_id      = c_nota.lstrip('0')
		str_number   = str(int(last_id) + 1)
		last_id      = str_number.rjust(5,'0')
		codigo      = last_id
	    else :
		str_number = '1'
		last_id      = str_number.rjust(5,'0')
		codigo      = last_id
	    return codigo
	
    """
    Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
    """
    def elimina_tildes(self, s):
    
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    
    """
    Metodo que trae la informacion de cada Ente/Organizacion.
    """
    def on_change_entes(self, cr, uid, ids, organismo, context=None):
        values = {}
        if not organismo:
            return values
        datos = self.pool.get('organos.entes').browse(cr, uid, organismo, context=context)
        values.update({
            'domicilio' : datos.direccion,
            'responsable' : datos.nom_responsable,
            'cargo' : datos.cargo,
            'telefono': datos.telefono,
            'correo': datos.correo,
	    'ubicacion': datos.direccion,
     
        })
        return {'value' : values}    

    def on_change_total(self, cr, uid, ids, bene_femenino, bene_masculino, context=None):

        values = {}
        total = int(bene_femenino) + int(bene_masculino)
        values.update({'bene_total' : total,})
        return {'value' : values} 

    def on_change_total_estimado(self, cr, uid, ids, empleos_directos_f, empleos_directos_m, context=None):

        values = {}
        est_total = int(empleos_directos_f) + int(empleos_directos_m)
        values.update({'t_emple_directos' : est_total,})
        return {'value' : values} 



    """
    Metodo con el cual genero el archivo .pdf 
    """

    def reporte_anteproyecto(self, cr, uid, ids, context=None): # Generacion de inventario

	# Instancia de la clase heredada L es horizontal y P es vertical
	# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)

	pdf=class_pdf.PDF(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
	
	#pdf.set_title(title)
	pdf.set_author('Marcel Arcuri')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	#pdf.set_font('Times','',10) # TAMANO Y TIPO DE LETRA DE LA FUENTE
	pdf.set_font('Arial','B',15)
	pdf.set_fill_color(157,188,201) # COLOR DE BORDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	#pdf.set_margins(8,10,10) # MARGENES DEL DOCUMENTO
	#pdf.ln(20) # Saldo de linea
	# 10 y 50 eje x y y 200 dimencion
	#pdf.line(10, 40, 200, 40) Linea
	proyect = self.browse(cr, uid, ids, context=context)
	npro = ""
	amb = ""
	for x in proyect:
	    ente = x.organismo.nombre_ente.encode("UTF-8").decode("UTF-8")
	    fec = x.f_solicitud.encode("UTF-8").decode("UTF-8")
	    domici = x.domicilio.encode("UTF-8").decode("UTF-8")
	    resp = x.responsable.encode("UTF-8").decode("UTF-8")
	    cargo = x.cargo.encode("UTF-8").decode("UTF-8")
	    tel = x.telefono.encode("UTF-8").decode("UTF-8")
	    
	    proyecto = x.nombre_pro.encode("UTF-8").decode("UTF-8")
	    dura = x.duracion.encode("UTF-8").decode("UTF-8")
	    inicio = x.f_inicio.encode("UTF-8").decode("UTF-8")
	    fin = x.f_fin.encode("UTF-8").decode("UTF-8")
	    
	    if x.etapa == 1:
		etapa = "Nueva"
	    else:
		etapa = "Continuación"
	    
	    if x.proy_nuevo == False:
		npro = ""
	    else:
		npro = x.proy_nuevo.encode("UTF-8").decode("UTF-8")
	    
	    costo = float(x['costo_proyecto'])
	    
	    fuente = x.fuente_fin.encode("UTF-8").decode("UTF-8")
	    indi = x.indicador.encode("UTF-8").decode("UTF-8")
	    form = x.formula.encode("UTF-8").decode("UTF-8")
	    verificacion = x.m_verificacion.encode("UTF-8").decode("UTF-8")
	    espe = x.especifique.encode("UTF-8").decode("UTF-8")

	    if int(x.ambito) == 1:
		amb = "Internacional"
	    elif int(x.ambito) == 2:
		amb = "Nacional"
	    elif int(x.ambito) == 3:
		amb = "Estadal"
	    elif int(x.ambito) == 4:
		amb = "Municipal"
	    elif int(x.ambito) == 5:
		amb = "Parroquia"
	    elif int(x.ambito) == 6:
		amb = "Sin Extensión Territorial"

	    plan = x.plan_patria.plan_patria.encode("UTF-8").decode("UTF-8")
	    obj_h = x.obj_historico.objetivo_historico.encode("UTF-8").decode("UTF-8")
	    obj_n = x.obj_nacional.objetivo_nacional.encode("UTF-8").decode("UTF-8")
	    obj_e = x.obj_estrategico.objetivo_estrategico.encode("UTF-8").decode("UTF-8")
	    obj_g = x.obj_general_plan.objetivo_general.encode("UTF-8").decode("UTF-8")
	    


	    
	    
	    
	    
	    
	    plan_g = x.plan_gobierno.plan_gobierno.encode("UTF-8").decode("UTF-8")
	    linea_est = x.linea_estrategica.lineas_estrategicas.encode("UTF-8").decode("UTF-8")
	    area_inv = x.area_inversion.encode("UTF-8").decode("UTF-8")
	    tipo = x.tipo.estructura.encode("UTF-8").decode("UTF-8")
	    sector = x.sector.sectores.encode("UTF-8").decode("UTF-8")
	    problema = x.desc_problema.encode("UTF-8").decode("UTF-8")
	    obj_g_pro = x.obj_general.encode("UTF-8").decode("UTF-8")
	    impacto = x.imp_impacto.encode("UTF-8").decode("UTF-8")
	    bene_f = int(x.bene_femenino)
	    bene_m = int(x.bene_masculino)
	    bene_t = int(x.bene_total)

	    if int(x.reque_accion) == 1:
		r_accion = "SI"
	    else:
		r_accion = "NO"
	    if int(x.contri_accion) == 1:
		c_accion = "SI"
	    else:
		c_accion = "NO"
	    if int(x.conflicto) == 1:
		conflic = "SI"
	    else:
		conflic = "NO"
	    
	    int_r = x.institucion_req.nombre_ente.encode("UTF-8").decode("UTF-8")
	    int_c = x.contri_institucion.nombre_ente.encode("UTF-8").decode("UTF-8")
	    conf_int = x.institucion_conf.nombre_ente.encode("UTF-8").decode("UTF-8")
	    exp_r = x.explique_req.encode("UTF-8").decode("UTF-8")
	    exp_c = x.contri_explique.encode("UTF-8").decode("UTF-8")
	    conf_exp = x.explique_con_conf.encode("UTF-8").decode("UTF-8")

	    emp_dir_f = int(x.empleos_directos_f)
	    emp_dir_m = int(x.empleos_directos_m)
	    emp_dir_t = int(x.t_emple_directos)
	    emp_dir_i = int(x.empleados_indirectos)




	    pdf.set_y(43)
	    pdf.set_x(10)
	    #Encabezado principal
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"1. IDENTIFICACIÓN DEL PROPONENTE".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    #1. Identificación de proponente
	    pdf.cell(47,5,"1.1 Organismo/Ente/Empresa:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(82,5,ente,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(41,5,"1.2. Fecha de Elaboración:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,fec,'TBR',1,'L',1)
    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(23,5,"1.3. Domicilio:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(167,5,domici,'BTR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"1.4. Responsable:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(52,5,resp,'TBR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"1.5. Cargo:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(50,5,cargo,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(21,5,"1.6. Teléfono:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(21,5,tel,'BTR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"1.7. Correo Electrónico:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(152,5,"jose_solorzano@gmail.com".decode("UTF-8"),'TBR',1,'L',1)
	    
	    #2.Datos del Proyecto
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"2. DATOS DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(40,5,"2.1. Nombre del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(150,5,proyecto,'TBR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(23,5,"2.2. Ubicación:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(167,5,domici,'TBR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(22,5,"2.3. Duración:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(40,5,dura,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"Fecha de inicio:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(17,5,inicio,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(21,5,"Fecha de fin:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(17,5,fin,'TBR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"2.4. Etapa:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(30,5,str(etapa).decode("UTF-8"),'TBR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"Proyecto Nuevo:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(62,5,npro,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"2.5. Costo del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(62,5,str(costo)+""+"Bs.",'BTR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(48,5,"2.6. Fuente de Financiamiento:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(54,5,fuente,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(35, 5,"2.7. Indicador General: ".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(53,5,indi,'BTR',1,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(55,5,"2.8. Fórmula del Indicador General:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(47,5,form,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(40, 5,"2.9. Medio de Verificación:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(48,5,verificacion,'BTR',1,'L',1)
	    
	    #3.LOCALIZACIÓN POLÍTICO ADMINISTRATIVA
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"3. LOCALIZACIÓN POLÍTICO ADMINISTRATIVA".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,5,"3.1. Ámbito:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(35,5,str(amb).decode("UTF-8"),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(27, 5,"3.2. Específique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(108,5,espe,'BTR',1,'L',1)
	    
	    #4.ÁREA ESTRATÉGICA
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4. ÁREA ESTRATÉGICA".decode("UTF-8"),'LTBR',1,'C',1)
	    #4.1
	    pdf.cell(190,5,"4.1. "+plan,'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(45,10,"4.1.1. Objetivo Histórico:".decode("UTF-8"),'LT',0,'L',0)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(145,5,obj_h,'TBR',0,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(45,5,"4.1.2. Objetivo Nacional:".decode("UTF-8"),'LT',0,'L',0)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(145,5,obj_n,'TBR',0,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(45,5,"4.1.3. Objetivo Estratégico:".decode("UTF-8"),'LT',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(145,5,obj_e,'TBR',0,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(45,15,"4.1.4. Objetivo General:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(145,5,obj_g,'TBR',0,'J',0)
	    
	    
	    #4.2
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4.2. "+plan_g,'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(75,5,"4.2.1. Lineas Estratégicas del Plan de Gobierno:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(115,5,linea_est,'TBR',1,'J',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"4.2.2. Área de Inversión:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(65,5,area_inv,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(21, 5,"4.2.3. Sector:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(66,5,sector,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"4.2.4. Tipo:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(172,5,tipo,'TBR',1,'J',1)
	    
	    
	    #5.
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"5. IDENTIFICACIÓN DEL PROBLEMA Y JUSTIFICACIÓN".decode("UTF-8"),'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.1 Descripción del problema:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,problema,'LBR',0,'J',0)
	    
	    
	    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	    pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	    pdf.set_y(43)
	    pdf.set_x(10)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.2. Objetivo General ".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_g_pro,'LBR',0,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.1. Importancia e Impacto".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,impacto,'LBR',0,'J',0)


	    #6.
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"6. POBLACIÓN BENEFICIADA POR LA EJECUCIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(47,5,"6.1. Beneficiarios Femeninos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(19,5,str(bene_f),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(47,5,"6.2. Beneficiarios Masculinos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(19,5,str(bene_m),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"6.3. Total Beneficiarios:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,str(bene_t),'TBR',1,'L',1)
	    
	    #7
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"7. CONEXIONES INTER-INSTITUCIONALES".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(90,5,"7.1. Requiere acciones (no financieras) de otra Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(100,5,r_accion,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.1.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,int_r,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.1.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,exp_r,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(100,5,"7.2. Contribuye o complementa acciones de otras instituciones:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(90,5,c_accion,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.2.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,int_c,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.2.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,exp_c,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(65,5,"7.3. Entra en conflicto con otra Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(125,5,conflic,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.3.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,conf_int,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.3.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,conf_exp,'BTR',1,'L',1)

	    #8.

	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"8. EMPLEADOS ESTIMADOS POR LA EJECUCIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(75,5,"8.1. N° Estimado de empleos directos femeninos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,str(emp_dir_f),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(77, 5,"8.2. N° Estimado de empleos directos masculinos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(18,5,str(emp_dir_m),'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(70,5,"8.3. N° Estimado totales de empleos directos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(25,5,str(emp_dir_t),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(60, 5,"8.2. N° Estimado de empleos directos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(35,5,str(emp_dir_i),'BTR',1,'L',1)
	    
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"9. ACCIONES ESPECÍFICAS".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    #9.
	    pdf.set_y(158)
	    pdf.set_x(10)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(55,8,"Nombre de la Acción Específica".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(158)
	    pdf.set_x(65)
	    pdf.cell(35,8,"Unidad de Medida".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(158)
	    pdf.set_x(100)
	    pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(158)
	    pdf.set_x(120)
	    pdf.cell(60,4,"Distribución Trimestral".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(162)
	    pdf.set_x(120)
	    pdf.set_font('Arial','',9)
	    pdf.cell(15,4,"I".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"II".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"III".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"IV".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(158)
	    pdf.set_x(180)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,8,"Total".decode("UTF-8"),'LTBR',1,'C',1)
	    
	    for i in range(1,5):
		pdf.set_font('Arial','',8)
		pdf.cell(55,5,"".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(35,5,"".decode("UTF-8"),'LBTR',0,'L',1)
		pdf.cell(20, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(20,5,"".decode("UTF-8"),'LBTR',1,'L',1)
	    
	    #10
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"10. METAS FINANCIERAS".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_y(191)
	    pdf.set_x(10)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(110,8,"Nombre de la Acción Específica".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(191)
	    pdf.set_x(120)
	    pdf.cell(60,4,"Distribución Trimestral".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(195)
	    pdf.set_x(120)
	    pdf.set_font('Arial','',9)
	    pdf.cell(15,4,"I".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"II".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"III".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"IV".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(191)
	    pdf.set_x(180)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,8,"Total".decode("UTF-8"),'LTBR',1,'C',1)
	    
	    for i in range(1,7):
		pdf.set_font('Arial','',8)
		pdf.cell(110,5,"".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(20,5,"".decode("UTF-8"),'LBTR',1,'L',1)

	    
	    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	    pdf.add_page() # AÑADE UNA NUEVA PAGINACIO

	    #11
	    pdf.set_y(43)
	    pdf.set_x(10)
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"11. IMPUTACIÓN PRESUPUESTARIA".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_y(48)
	    pdf.set_x(10)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(30,8,"Código".decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.cell(80,8,"Partida Presupuestaria".decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.set_y(48)
	    pdf.set_x(120)
	    pdf.cell(60,4,"Distribución Trimestral".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(52)
	    pdf.set_x(120)
	    pdf.set_font('Arial','',9)
	    pdf.cell(15,4,"I".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"II".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"III".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"IV".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_y(48)
	    pdf.set_x(180)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,8,"Total".decode("UTF-8"),'LTBR',1,'C',1)
	    
	    for i in range(1,10):
		pdf.set_font('Arial','',8)
		pdf.cell(30,5,"".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(80,5,"".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(15, 5,"".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(20,5,"".decode("UTF-8"),'LBTR',1,'L',1)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(110,5,"Totales".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(15, 5,"0.00".decode("UTF-8"),'LTB',0,'R',1)
	    pdf.cell(15, 5,"0.00".decode("UTF-8"),'LTB',0,'R',1)
	    pdf.cell(15, 5,"0.00".decode("UTF-8"),'LTB',0,'R',1)
	    pdf.cell(15, 5,"0.00".decode("UTF-8"),'LTB',0,'R',1)
	    pdf.cell(20,5,"0.00".decode("UTF-8"),'LBTR',1,'R',1)
	    
	    #nom = nombre+" "+str(fec)+'.pdf' #Nombre del archivo .pdf
	    
	    #nom = proyecto+" "+str(fec)+'.pdf'
	    
	#    pdf.output('openerp/addons/producto_bva/reporte/'+nom,'F') #Carpeta donde se guardara
	#	
	#	archivo = open('openerp/addons/producto_bva/reporte/'+nom)
	    pdf.output('home/administrador/openerp70/modules/planificacion_presupuesto/reportes/Conaplan.pdf','F')

	    archivo = open('home/administrador/openerp70/modules/planificacion_presupuesto/reportes/Conaplan.pdf')

	    """
	    Mandamos el archivo al modelo de reportes, donde se iran almacenando
	    """
	    r_archivo = self.pool.get('reportes.presupuesto').create(cr, uid, {
		    'name' : nom,
		    'res_name' : nom,
		    'datas' : base64.encodestring(archivo.read()),
		    'datas_fname' : nom,
		    'res_model' : 'reportes.presupuesto',
		    'registro': "Anteproyecto",
		    },context=context)

	    return r_archivo
	
	    
	    
    _columns = {
        'c_solicitud' : fields.char(string="ID", size=255, required=False, readonly=True),
	'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
	#'archivos': fields.function(_data_get, fnct_inv=_data_set, string='Cargar Archivos', type="binary", nodrop=True),
	'archivos': fields.binary('Adjuntar Archivo'),
	
	#Pestaña1
	'organismo': fields.many2one('organos.entes', 'Organismo/Ente/empresa:', required=True),
        'f_solicitud': fields.char('Fecha de Elaboración:', required=True, readonly=True),
	'domicilio': fields.char('Domicilio:', required=True),
	'responsable': fields.char('Responsable:', required=True),
	'cargo': fields.char('Cargo:', required=True),
	'telefono': fields.char('Teléfono:', required=True),
	'correo': fields.char('Correo Electrónico:', required=True),
	#Pestaña2
	'nombre_pro': fields.char('Nombre del Proyecto', required=True),
	'ubicacion': fields.char('Ubicación',  required=True),
	'duracion': fields.char('Duración',  required=True),
	'f_inicio': fields.date('Fecha de Inicio', required=True),
	'f_fin': fields.date('Fecha de Finalización', required=True),
	'etapa': fields.selection([('1','Nueva'), ('2','Continuación')], string="Etapa", required=True),
	'proy_nuevo': fields.char('Proyecto Nuevo', required=False),
	'costo_proyecto': fields.float('Costo del Proyecto', readonly=False),
	'fuente_fin': fields.char('Fuente de Financiamiento:',  required=True),
	'indicador': fields.char('Indicador General', required=True),
	'formula': fields.char('Fórmula del Indicador General:', required=True),
	'm_verificacion': fields.char('Medio de Verificación:', required=False),
	#Pestaña3
	'ambito': fields.selection([('1','Internacional'), ('2','Nacional'), ('3','Estadal'), ('4','Municipal'), ('5','Parroquia'),('6','Sin Extensión Territorial')], string="Ámbito"),
	'especifique': fields.text('Específique:', required=False),
	#Pestaña4
	'obj_general_plan' : fields.many2one('objetivo.general', 'Objetivos Generales', required=False),
	'obj_estrategico' : fields.many2one('objetivo.estrategico', 'Objetivos Estratégico', required=False),
	'obj_nacional' : fields.many2one('objetivo.nacional', 'Objetivos Nacional', required=False),
	'obj_historico' : fields.many2one('objetivo.historico', 'Objetivos Historicos', required=False),
	'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=False),
	'plan_gobierno': fields.many2one('plan.gobierno', 'Plan de Gobierno', required=False),
	'linea_estrategica': fields.many2one('lineas.estrategicas', 'Lineas estrategicas de Accion', required=False),
	'area_inversion': fields.char('Área de Inversión:', required=False),
	'tipo':fields.many2one('tipo.estructura', 'Tipo', ondelete='cascade', select=False),
	'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False),
	#Pestaña 5
	'desc_problema': fields.text('Descripción del problema:', required=False),
	'obj_general': fields.text('Objetivo General:', required=False),
	'imp_impacto': fields.text('Importancia e Impacto:', required=False),
	#Pestaña 6
	'bene_femenino': fields.integer('Beneficiarios Femeninos:', required=False),
	'bene_masculino': fields.integer('Beneficiarios Masculinos:', required=False),
	'bene_total': fields.integer('Beneficiarios Totales:', required=False, readonly=False),
	#Pestaña 7
	'reque_accion': fields.selection([('1','SI'), ('2','NO')], string="7.1. Requiere acciones (no financieras) de otra institución:"),
	'institucion_req': fields.many2one('organos.entes', 'Institución:', required=False),
	'explique_req': fields.char('Explique:', required=False),
	'contri_accion': fields.selection([('1','SI'), ('2','NO')], string="7.2. Contribuye o complementa acciones de otras instituciones:"),
	'contri_institucion': fields.many2one('organos.entes', 'Institución:', required=False),
	'contri_explique': fields.char('Explique:', required=False),
	'conflicto': fields.selection([('1','SI'), ('2','NO')], string="7.3. Entra en conflicto con otras instituciones:"),
	'institucion_conf': fields.many2one('organos.entes', 'Institución:', required=False),
	'explique_con_conf': fields.char('Explique:', required=False),
	#pestaña8
	'empleos_directos_f': fields.integer('N° Estimado de empleaos directos femeninos:', required=False),
	'empleos_directos_m': fields.integer('N° Estimado de empleaos directos masculinos:', required=False),
	't_emple_directos': fields.integer('N° Estimado totales de empleos directos:', required=False, readonly=False),
	'empleados_indirectos': fields.integer('N° Estimado de empleos indirectos:', required=False),
	#pestañas9
	'acciones_especificas':fields.one2many('acciones.especificas', 'acciones_ids',required=False),
	#pestañas10
	'metas_financieras':fields.one2many('metas.financieras', 'metas_ids',required=False),
	#pestañas11
	'imputacion_presu':fields.one2many('imputacion.presupuestaria', 'imputacion_ids',required=False),

        }
        
        
    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        'c_solicitud': _get_last_id,
        'user_register': lambda s, cr, uid, c: uid,
  
    }