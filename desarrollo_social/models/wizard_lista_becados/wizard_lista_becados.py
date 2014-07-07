# -*- coding: utf-8 -*-

from osv import osv,fields

class CrearWizardBecados(osv.TransientModel):
	_name = 'becados.crear.wizard'
	
	#Método para crear las nóminas individuales a partir de los becados seleccionados
	def action_add_becado(self, cr, uid, ids, context=None):
		nominaindividual_model = self.pool.get('becados.nominaindividual')
		wizard = self.browse(cr, uid, ids[0], context=context)
		for becado in wizard.becados:
			print becado.name
			nominaindividual_model.create(cr, uid, {
				'nomina': '10',
				'becado': becado.id, 
			})
		return {}		
	
	_columns = {
		'becados' : fields.many2many("hr.employee", "seleccion_becados", "becados_wizard_id", "hr_employee_id", "Becados", required = True, domain=[('categoria','=','1'),('status','=','1')]),
	}

class WizardBecados():
	_name = 'becados.wizard'
	
	_columns = {
		'wizard_id' : fields.many2one("becados.crear.wizard","wizard_id"), 
	}
