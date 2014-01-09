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

############################
# Fondos de financiamiento #
############################

class gdc_fondos(osv.Model):
    """
    Modelo para gestionar los fondos de financiamiento
    """
    _name = "gdc.fondos"
    _rec_name = "name"
    _order="name"

    _columns = {
        'name': fields.char(string="Fondo de financiamiento", size=64, required=True), 
    }

#############
# Proyectos #
#############

class gdc_proyectos(osv.Model):
    """
    Modelo para gestionar las actividades
    """
    _name = "gdc.proyectos"
    _rec_name = "actividad"
    _order="actividad"
    
    def on_change_address_id(self, cr, uid, ids, address_id, context=None):
        """
        Onchange para traer toda la informacion de la direccion
        """
        values = {}
        if not address_id:
            return values
        address = self.pool.get('res.partner').browse(cr, uid, address_id, context=context)
        values.update({
            'street' : address.street,
            'street2' : address.street2,
            'city' : address.city,
            'country_id' : address.country_id and address.country_id.id or False,
            'state_id' : address.state_id and address.state_id.id or False,
            'zip' : address.zip,
        })
        return {'value' : values}
    
    def onchange_date_start(self, cr, uid, ids, date_start, context=None):
        """
        Onchange para validar que la fecha de inicio no es menor a la 
        fecha de creacion
        """
        res = {}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
        if date_start < now:
            res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha de inicio dias pasados",}
            return res
        return res
        
    def onchange_date_end(self, cr, uid, ids, date_end, context=None):
        """
        Onchange para validar que la fecha final no es menor a la 
        fecha de creacion
        """
        res = {}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if date_end < now:
            res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha final dias pasados",}
            return res
        return res
            
    def _compute_days(self, cr, uid, ids, field, arg, context=None):
        """
        Metodo para calcular los dias entre la fecha de inicio y la fecha final
        """
        import datetime
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            if r.date_start:
                d = time.strptime(r.date_start,'%Y-%m-%d %H:%M:%S')
        for r2 in records:
            if r2.date_end:
                c = time.strptime(r2.date_end,'%Y-%m-%d %H:%M:%S')
                delta = datetime.datetime(c[0], c[1], c[2]) - datetime.datetime(d[0], d[1], d[2])
                weeks, days = divmod(delta.days, 1)
            result[r2.id] = weeks
        return result

    def copy(self, cr, uid, id, default, context=None):
        """
        Metodo para realizar la copia de proyectos
        """
        proyecto = self.browse(cr, uid, id, context=context)
        new_name = "Copia de %s" % proyecto.actividad
        others_count = self.search(cr, uid, [('actividad', '=like', new_name+'%')], count=True, context=context)
        if others_count > 0:
            new_name = "%s (%s)" % (new_name, others_count+1)
        default['actividad'] = new_name
        return super(gdc_proyectos, self).copy(cr, uid, id, default, context=context)

    _columns = {
        'date_created': fields.char('Fecha de Creación',select=True, readonly=True),
        'codigo': fields.char(string="Codigo", size=20),  
        'actividad': fields.char(string="Actividad", size=64, required=True), 
        'cobertura': fields.selection((('Direccionalidad','Direccionalidad'),('Nacional','Nacional'), ('Regional','Regional'), ('Municipal', 'Municipal')),'Cobertura', required=True),
        'priority': fields.selection((('Baja','Baja'), ('Normal','Normal'), ('Alta', 'Alta')),'Prioridad', required=True),
        'tipo_financiamiento': fields.many2one('gdc.fondos', 'Fondos de finaciamiento', required=True),
        'estado': fields.selection((('Borrador','Borrador'), ('Progreso', 'Progreso'), ('Terminado', 'Terminado'), ('Congelado', 'Congelado'), ('Vencido', 'Vencido')),'Estado', required=True),
        'progreso': fields.float(string="Progreso"), 
        'dias_proyecto': fields.function(_compute_days, type='char', string='Dias asignados al proyecto'),
        'date_start': fields.datetime('Fecha estimada de inicio',select=True, required=True),
        'date_end': fields.datetime('Fecha estimada de finalizacion',select=True, required=True),
        'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=[('category_id.name','ilike','Responsable')], required=True),
        'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=True),
        'description': fields.text('Description', required=True),
        'presu_tentativo': fields.float('Presupuesto Tentativo  (Bs.)'),
        'presu_real': fields.float('Presupuesto Real (Bs.)'),
        'bene_tentativo': fields.integer('Cantidad de beneficiados tentativos', required=True),
        'members_project': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Instituciones'),
        'address_id': fields.many2one('res.partner','Lugar', readonly=False, required=True, domain=[('category_id.name','ilike','Lugar')]),
        'street': fields.related('address_id','street',type='char',string='Direccion'),
        'street2': fields.related('address_id','street2',type='char',string='Cont. Direccion'),
        'state_id': fields.related('address_id','state_id',type='many2one', relation="res.country.state", string='Estado'),
        'zip': fields.related('address_id','zip',type='char',string='Codigo Postal'),
        'city': fields.related('address_id','city',type='char',string='Ciudad'),
        'country_id': fields.related('address_id', 'country_id', type='many2one', relation='res.country', string='Pais', readonly=False),
        'tareas_ids': fields.one2many('gdc.tareas', 'project_id2', string="Tareas"),
        'incidencias_ids': fields.one2many('gdc.incidencias', 'tarea_id', string="Incidencias"),
        'conclusiones': fields.text('Conclusiones'),
        'acuerdos': fields.text('Acuerdos'),
        'incidencias': fields.text('Incidencias'),
        'adjunto_gaceta': fields.binary('Adjuntar Gaceta digital'),
    }
        
    def _check_dates_now(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que la fecha de inicio 
        debe ser mayor o igual a la fecha de creacion del proyecto
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for leave in self.read(cr, uid, ids, ['date_start'], context=context):
            if leave['date_start']:
                if leave['date_start'] <= now:
                    return False
        return True
        
    def _check_dates(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
            if leave['date_start'] and leave['date_end']:
                if leave['date_start'] > leave['date_end']:
                    return False
        return True

    _constraints = [
        (_check_dates_now, 'Error! La fecha de inicio debe ser mayor o igual a la fecha de creacion del proyecto', ['date_start']),
        (_check_dates, 'Error! La fecha de inicio debe ser menor que la fecha final.', ['date_start', 'date_end']),
    ]
    
    _sql_constraints = [
        ('actividad_unique','UNIQUE(actividad)','La actividad debe ser unica. Intente copiar el proyecto'),
    ]
    
    _defaults = {
            'supervisor_id': 1,
            'codigo': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'gdc.proyectos'),
            'estado': 'Borrador',
            'progreso': 0.0,
            'date_created': lambda *a: datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'dias_proyecto': 'Aun no asignados. ',
            'priority': 'Baja',
    }

    def congelar_proyecto(self, cr, uid, ids, context=None):
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'estado': 'Congelado'})
        
    def retomar_proyecto(self, cr, uid, ids, context=None):
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'estado': 'Progreso'})

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
        res = {}
        gdc_project = self.pool.get('gdc.proyectos')
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            gdc_project_src = gdc_project.read(cr, uid, r.project_id2.id, ['supervisor_id'], context)
            if gdc_project_src['supervisor_id']:
                self.write(cr, uid, ids, {'supervisor_id': gdc_project_src['supervisor_id'][0]})
            return res
            
    def onchange_date_start_tarea(self, cr, uid, ids, date_start_tarea, context=None):
        res = {}
        gdc_project = self.pool.get('gdc.proyectos')
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            gdc_project_src = gdc_project.read(cr, uid, r.project_id2.id, ['date_start'], context)
            if date_start_tarea < gdc_project_src['date_start']:
                res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas menores a la inicio del proyecto.",}
                return res
            return res

    def onchange_date_end_tarea(self, cr, uid, ids, date_end_tarea, context=None):
        res = {}
        gdc_project = self.pool.get('gdc.proyectos')
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            gdc_project_src = gdc_project.read(cr, uid, r.project_id2.id, ['date_end'], context)
            if date_end_tarea > gdc_project_src['date_end']:
                res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas mayores a la final del proyecto.",}
                return res
            return res

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
        'name_tarea': fields.char(string="Tarea", size=50, required=False),
        'project_id2': fields.many2one('gdc.proyectos', 'Asignacion', required=False),
        'estado_tarea': fields.selection((('Borrador','Borrador'), ('Progreso', 'Progreso'), ('Terminado', 'Terminado'), ('Congelado', 'Congelado'), ('Vencido', 'Vencido')),'Estado', required=True),
        'date_start_tarea': fields.datetime('Fecha de inicio',select=True),
        'date_end_tarea': fields.datetime('Fecha de finalizacion',select=True),
        'progreso_tarea': fields.float(string="Progreso de tarea"), 
        'dias_tarea': fields.function(_compute_days_tarea, type='char', string='Dias asignados a la tarea'),
        'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=['|',('is_company','=',False),('category_id.name','ilike','Responsable')], required=False),
        'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=True),
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

###############
# Incidencias #
###############
    
class gdc_incidencias(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.incidencias"
    _rec_name = "name_incidencia"
    _order="name_incidencia"
    
    _columns = {
        'name_incidencia': fields.char(string="Incidencia", size=50, required=False),
        'tarea_id': fields.many2one('gdc.tareas', 'tarea', required=False),
        'date_reporter': fields.datetime('Fecha',select=True, required=True),
        'description': fields.text('Description'),
    }
