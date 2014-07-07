# -*- coding: utf-8 -*-
from fpdf import FPDF

import fpdf

#title='Encabezado con estilo'


class PDF(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',12)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		# Ruta local
		#~ self.image('openerp/addons/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		# Ruta servidor
		self.image('/home/administrador/openerp70/modules/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		#Calcular ancho del texto (title) y establecer posición
		#w=self.get_string_width(title)+6
		#self.set_x((210-w)/2)
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(0,0,0)
		
		self.set_y(10)
		self.set_x(70)
		self.set_font('Arial','',12)
		self.write(10,"***A.C. BIBLIOTECAS VIRTUALES DE ARAGUA")
		self.ln(6)
		self.set_y(20)
		self.set_x(70)
		self.set_font('Arial','B',12)
		self.write(10,"NÓMINA RESUMEN DE CONCEPTOS POR BANCO".decode("UTF-8"))
		self.ln(6)
				
		#Grosor del marco (1 mm)
		#self.set_line_width(1)
		#Titulo
		#self.cell(w,9,title,1,1,'C',1)
		#Salto de línea
		self.ln(-5)
		
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
		self.cell(190,-500,'Pág '.decode("UTF-8")+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R')
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
		#~ self.set_auto_page_break(auto, margin=0)
		
	# CONSTRUCCTOR DEL DOCUMENTO
	def print_chapter(self,num,title,name):
		self.add_page()
		self.chapter_title(num,title)
		self.chapter_body(name)



#CLASE PARA EL REPORTE DE RESUMEN DE NÓMINA
class PDF2(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',12)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		# Ruta local
		#~ self.image('openerp/addons/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		# Ruta servidor
		self.image('/home/administrador/openerp70/modules/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		#Calcular ancho del texto (title) y establecer posición
		#w=self.get_string_width(title)+6
		#self.set_x((210-w)/2)
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(0,0,0)
		
		self.set_y(12)
		self.set_x(70)
		self.set_font('Arial','',12)
		self.write(10,"***A.C. BIBLIOTECAS VIRTUALES DE ARAGUA")
		self.ln(6)
		self.set_y(22)
		self.set_x(90)
		self.set_font('Arial','B',12)
		self.write(10,"RESUMEN DE NÓMINA".decode("UTF-8"))
		self.ln(6)
				
		#Grosor del marco (1 mm)
		#self.set_line_width(1)
		#Titulo
		#self.cell(w,9,title,1,1,'C',1)
		#Salto de línea
		self.ln(-5)
		
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
		#~ self.cell(190,-500,'Pág '.decode("UTF-8")+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R')
		
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



#CLASE PARA EL REPORTE DE NÓMINA DETALLADO POR BANCO
class PDF3(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',12)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		# Ruta local
		#~ self.image('openerp/addons/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		# Ruta servidor
		self.image('/home/administrador/openerp70/modules/desarrollo_social/img/logo_bva2.jpg',8,12,50)
		#Calcular ancho del texto (title) y establecer posición
		#w=self.get_string_width(title)+6
		#self.set_x((210-w)/2)
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(0,0,0)
		
		self.set_y(10)
		self.set_x(70)
		self.set_font('Arial','',12)
		self.write(10,"***A.C. BIBLIOTECAS VIRTUALES DE ARAGUA")
		self.ln(6)
		self.set_y(20)
		self.set_x(76)
		self.set_font('Arial','B',12)
		self.write(10,"NÓMINA DETALLADO POR BANCO".decode("UTF-8"))
		self.ln(6)
				
		#Grosor del marco (1 mm)
		#self.set_line_width(1)
		#Titulo
		#self.cell(w,9,title,1,1,'C',1)
		#Salto de línea
		self.ln(-5)

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
		self.cell(190,-500,'Pág '.decode("UTF-8")+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R')
		
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

