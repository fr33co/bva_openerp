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

from openerp.osv import osv, fields

class gdc_sector(osv.Model):
    _name = "gdc.sector"
    _rec_name = "name_sector"
    _columns = {
            'name_sector' : fields.char(string="Sector", size=256, required=True),
    }
    
    _order="name_sector"
    
class gdc_caracterizacion(osv.Model):
    _name = "gdc.caracterizacion"
    _columns = {
            'ente': fields.selection((('s','Secretaria'), ('i','Institucion')),'Tipo de Ente', required=True),
            'institucion_id' : fields.many2one('res.company', 'Institucion', required=True),
            'responsible_id' : fields.many2one('res.users', 'Responsable de la institucion', required=True),
            'codigo': fields.char(string="Codigo", size=64),            
    }
    
