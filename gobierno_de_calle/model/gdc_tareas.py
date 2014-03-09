#-*- coding:utf-8 -*-
##############################################################################
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime
import time
from openerp.osv import osv, fields
from tools.translate import _

##########
# Tareas #
##########
    
class gdc_tareas(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.tareas"
    _rec_name = "name_tarea"
    _order="name_tarea"

    def onchange_proyecto(self, cr, uid, ids, project_id2, context=None):
        values = {}
        gdc_project = self.pool.get('gdc.proyectos')
        proyecto_brw = gdc_project.browse(cr, uid, project_id2, context=context)
        proyecto_rd = gdc_project.read(cr, uid, proyecto_brw.id, ['ejecutor_id', 'supervisor_id', 'responsible_id'], context=context)
        if proyecto_rd['supervisor_id'] and proyecto_rd['responsible_id']:
            values.update({
            'supervisor_id' : proyecto_rd['supervisor_id'][0],
            'responsible_id' : proyecto_rd['responsible_id'][0],
            'ejecutor_id' : proyecto_rd['ejecutor_id'][0],
            })
            return {'value' : values}
        else: 
            return values


    def onchange_date_start_tarea(self, cr, uid, ids, project_id2, date_start_tarea, context=None):
        values = {}
        gdc_project = self.pool.get('gdc.proyectos')
        proyecto_brw = self.browse(cr, uid, project_id2, context=context)
        gdc_project_rd = gdc_project.read(cr, uid, proyecto_brw.project_id2.id, ['date_start'], context)
        if date_start_tarea < gdc_project_rd['date_start']:
            values['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas menores a la inicio del proyecto.",}
            return values
        else:
            return values


    def onchange_date_end_tarea(self, cr, uid, ids, project_id2, date_end_tarea, context=None):
        values = {}
        gdc_project = self.pool.get('gdc.proyectos')
        proyecto_brw = self.browse(cr, uid, project_id2, context=context)
        gdc_project_rd = gdc_project.read(cr, uid, proyecto_brw.project_id2.id, ['date_end'], context)
        if date_end_tarea > gdc_project_rd['date_end']:
            values['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas mayores a la final del proyecto.",}
            return values
        else:
            return values


    def _compute_days_tarea(self, cr, uid, ids, field, arg, context=None):
        """
        Metodo para calcular los dias entre la fecha de inicio y la fecha final
        """
        import datetime
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            if r.date_start_tarea:
                d = time.strptime(r.date_start_tarea,'%Y-%m-%d %H:%M:%S')
        for r2 in records:
            if r2.date_end_tarea:
                c = time.strptime(r2.date_end_tarea,'%Y-%m-%d %H:%M:%S')
                delta = datetime.datetime(c[0], c[1], c[2]) - datetime.datetime(d[0], d[1], d[2])
                weeks, days = divmod(delta.days, 1)
            result[r2.id] = weeks
        return result
            
            
    _columns = {
        'name_tarea': fields.char(string="Tarea", size=50, required=True),
        'project_id2': fields.many2one('gdc.proyectos', 'Asignacion', required=True),
        'estado_tarea': fields.selection((('Borrador','Borrador'), ('Progreso', 'Progreso'), ('Terminado', 'Terminado'), ('Congelado', 'Congelado'), ('Vencido', 'Vencido')),'Estado', required=True),
        'date_start_tarea': fields.datetime('Fecha de inicio',select=True),
        'date_end_tarea': fields.datetime('Fecha de finalizacion',select=True),
        'progreso_tarea': fields.float(string="Progreso de tarea"), 
        'dias_tarea': fields.function(_compute_days_tarea, type='char', string='Dias asignados a la tarea'),
        'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=['|',('is_company','=',False),('category_id.name','ilike','Responsable')], required=False),
        'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=False),        
        'ejecutor_id' : fields.many2one('res.company', 'Ente Ejecutor', domain=[('category_id.name','ilike','Supervisor')], required=False),
        'members_tareas': fields.many2many('res.company', 'project_company_rel2', 'project_id2', 'uid2', 'Equipos de trabajo'),
        'description': fields.text('Description'),
        'informe_tareas': fields.binary('Informe'),
        'image': fields.binary("Foto", help="Seleccione una imagen"),
    }


    def _check_dates_tareas(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_start_tarea', 'date_end_tarea'], context=context):
            if leave['date_start_tarea'] and leave['date_end_tarea']:
                if leave['date_start_tarea'] > leave['date_end_tarea']:
                    return False
        return True


    _constraints = [
        (_check_dates_tareas, 'Error! La fecha de inicio debe ser menor que la fecha final.', ['date_start_tarea', 'date_end_tarea']),
    ]
    
    
    _defaults = {
            'estado_tarea': 'Borrador',
            'progreso_tarea': 0.0,
    }


    def begin_tarea(self, cr, uid, ids, context=None):
        result = {}
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        gdc_project = self.pool.get('gdc.proyectos')
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            gdc_project_src = gdc_project.read(cr, uid, r.project_id2.id, ['date_start', 'date_end', 'progreso', 'dias_proyecto'], context)
            if gdc_project_src['date_start'] <= r.date_start_tarea and gdc_project_src['date_end'] >= r.date_end_tarea and r.date_end_tarea > r.date_start_tarea:
                calculo = (100.0 * int(r.dias_tarea)) / int(gdc_project_src['dias_proyecto'])
                porcentaje = "%.2f" % calculo
                total = int(gdc_project_src['progreso']) + float(porcentaje)
                gdc_project.write(cr, uid, r.project_id2.id, {'progreso': total, 'estado': 'Progreso'})
                self.write(cr, uid, ids, {'estado_tarea': 'Progreso'})
                ini = time.strptime(r.date_start_tarea,'%Y-%m-%d %H:%M:%S')
                fin = time.strptime(r.date_end_tarea,'%Y-%m-%d %H:%M:%S')
                ahora = time.strptime(now,'%Y-%m-%d %H:%M:%S')
                if r.date_start_tarea and r.date_end_tarea:
                    delta_1 = datetime.datetime(ini[0], ini[1], ini[2]) - datetime.datetime(ahora[0], ahora[1], ahora[2])
                    calculo_delta1 = (100.0 * int(delta_1.days)) / int(r.dias_tarea)
                    print calculo_delta1
                    delta_2 = datetime.datetime(fin[0], fin[1], fin[2]) - datetime.datetime(ahora[0], ahora[1], ahora[2])
                    calculo_delta2 = (100.0 * int(delta_2.days)) / int(r.dias_tarea)
                    print calculo_delta2
                    self.write(cr, uid, ids, {'progreso_tarea': calculo_delta1})
                else:
                    if now >= r.date_start_tarea and r.date_end_tarea:
                        self.write(cr, uid, ids, {'progreso_tarea': 100.0})
                    else:
                        self.write(cr, uid, ids, {'progreso_tarea': 0.0})
            else: 
                result['warning'] = {'title': "Cuidado: Error!",'message' : "Fechas asignadas de forma incorrecta.",}
                return result

    def finish_tarea(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'estado_tarea': 'Terminado', 'progreso_tarea': 100.0})


