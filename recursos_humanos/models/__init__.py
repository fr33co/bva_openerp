# -*- coding: utf-8 -*-

import empleado
import proceso_nomina # Proceso de Generación de nóminas (Masivo)
import contrato
import concepts # Sub modulo de conceptos
import carga_familiar_employee #Carga Familiar
import profesion_oficio
import degree # Sub modulo de grado
import selection
import change_status # Cambio de estatus
import change_salary_employee
#import onchange_slip # Cambio de nomina
import hr_departament # Departamento a cargo de las Gerencias
import hr_bank # Sub modulo de entidad bancaria (Herencia)
import hr_document # Importacion del sub modulo para adjuntar reportes
import payslip
import update_employee # Importacion del sub modulo cambio de estatus
import shuttle_ascent_employee # Importacion del sub modulo de Traslado y/o Ascenso a empleados
import charge # herencia de Cargo
import movement_employee # Importacion del sub modulo asignacion de movimientos a empleados
import asignacion_nomina_regular # Importacion del sub modulo asignacion de nomina regular (conceptos) one2many
import asignacion_nomina_vacaciones # Importacion del sub modulo asignacion de nomina vacaciones (conceptos) one2many
import nomina
import configuracion_asignacion
import propietario
import hr_ticket # Nomina de cesta Ticket
import hr_asig_alimentacion # Asignacion / Alimentacion