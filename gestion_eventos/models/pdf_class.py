# -*- coding: utf-8 -*-
from fpdf import FPDF
import fpdf
#####################################################################################################
#				CLASE CONSTRUCTORA DETALLADO DE LAS ACTIVIDADES
#####################################################################################################
#title='Encabezado con estilo'

class Detallado(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		# LOCAL
		#~ self.image('openerp/addons/gestion_eventos/img/gob.jpg',5,10,50) # Imagen Izquierda
		#~ self.image('openerp/addons/gestion_eventos/img/logo_bva2.jpg',220,15,50) # Imagen Derecha
		# self.image('openerp/addons/gestion_eventos/img/footer.jpg',220,15,50) # Imagen Footer
		
		# SERVIDOR
		self.image('/home/administrador/openerp70/modules/gestion_eventos/img/gob.jpg',5,10,50) # Imagen Superior
		self.image('/home/administrador/openerp70/modules/gestion_eventos/img/logo_bva2.jpg',220,15,50) # Imagen Indferior
		
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(220,50,50)
		self.ln(20)

		
		#METODO PARA CONSTRUIR LA PAGINACION
		# Page footer
	def footer(self):
		#Posición a 1.5 cm desde abajo
		self.set_y(-15)
		#Arial italic 8
		self.set_font('Arial','I',8)
		#Color de texto en gris
		self.set_text_color(128)
		#Numero de pagina
		self.cell(0,10,'Pagina '+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R') 
		
	def chapter_title(self,num,label):
		#Arial 12
		self.set_font('Arial','',12)
		#Color de fondo
		self.set_fill_color(200,220,255)
		#Titulo
		self.cell(0,6,"Chapter %d : %s"%(num,label),0,1,'L',1)
		#Salto de línea
		self.ln(4)
		
	def chapter_body(self,name):
		#Leer archivo de texto
		txt=file(name).read()
		#Times 12
		self.set_font('Times','',12)
		#Emitir texto justificado
		self.multi_cell(0,5,txt)
		#Salto de línea
		self.ln()
		#Mención en italic -cursiva-
		self.set_font('','I')
		self.cell(0,5,'(end of excerpt)')
		
	# CONSTRUCCTOR DEL DOCUMENTO
	def print_chapter(self,num,title,name):
		self.add_page()
		self.chapter_title(num,title)
		self.chapter_body(name)
		
##########################################################################################
class Fotos(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		# LOCAL
		self.image('openerp/addons/gestion_eventos/img/gob.jpg',5,10,50) # Imagen Izquierda
		self.image('openerp/addons/gestion_eventos/img/logo_bva2.jpg',150,15,50) # Imagen Derecha
		# self.image('openerp/addons/gestion_eventos/img/footer.jpg',220,15,50) # Imagen Footer
		
		# SERVIDOR
		#self.image('/home/administrador/openerp70/modules/gestion_eventos/img/gob.jpg',5,10,50) # Imagen Superior
		#self.image('/home/administrador/openerp70/modules/gestion_eventos/img/logo_bva2.jpg',220,15,50) # Imagen Indferior
		
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(220,50,50)
		self.ln(20)

		
		#METODO PARA CONSTRUIR LA PAGINACION
		# Page footer
	def footer(self):
		#Posición a 1.5 cm desde abajo
		self.set_y(-15)
		#Arial italic 8
		self.set_font('Arial','I',8)
		#Color de texto en gris
		self.set_text_color(128)
		#Numero de pagina
		self.cell(0,10,'Pagina '+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R') 
		
	def chapter_title(self,num,label):
		#Arial 12
		self.set_font('Arial','',12)
		#Color de fondo
		self.set_fill_color(200,220,255)
		#Titulo
		self.cell(0,6,"Chapter %d : %s"%(num,label),0,1,'L',1)
		#Salto de línea
		self.ln(4)
		
	def chapter_body(self,name):
		#Leer archivo de texto
		txt=file(name).read()
		#Times 12
		self.set_font('Times','',12)
		#Emitir texto justificado
		self.multi_cell(0,5,txt)
		#Salto de línea
		self.ln()
		#Mención en italic -cursiva-
		self.set_font('','I')
		self.cell(0,5,'(end of excerpt)')
		
	# CONSTRUCCTOR DEL DOCUMENTO
	def print_chapter(self,num,title,name):
		self.add_page()
		self.chapter_title(num,title)
		self.chapter_body(name)
