# -*- coding: utf-8 -*-

import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from openerp.tools.translate import _

class tipo_estructura(osv.Model):

	_name = "tipo.estructura"
	
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('tipo.estructura')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['codigo']
                    c_nota = id_documento[:]
                    last_id      = c_nota.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(2,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(2,'0')
                    codigo      = last_id
                return codigo

	_rec_name ="estructura"

	_columns = {
		'codigo' : fields.char(string="Código", required=False, readonly=True),
		'estructura' : fields.char(string="Estructura", required=False),

	}
	_defaults = {
		'codigo' : _get_last_id
	} 