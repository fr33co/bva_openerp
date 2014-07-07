# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class organos_sectores(osv.Model):

	_name = "organos.sectores"
	
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('organos.sectores')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['codigo']
                    c_sec = id_documento[:]
                    last_id      = c_sec.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(2,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(2,'0')
                    codigo      = last_id
                return codigo


	_rec_name = "sectores"
	_columns = {
		'codigo' : fields.char(string="Código", required=False,  readonly=True),
		'sectores' : fields.char(string="Sector", required=False),

	}
	_defaults = {
		'codigo' : _get_last_id
	} 