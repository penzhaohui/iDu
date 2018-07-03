# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
import logging
import datetime
import time

_logger = logging.getLogger(__name__)

class Abstract(models.AbstractModel):
    _name = 'openacademy.abstract'
    field1 = fields.Boolean()

    def doSomething(self):
        print 'Abstract'

class Abstract2(models.AbstractModel):
    _inherit = 'openacademy.abstract'
    field2 = fields.Boolean()

    def doSomething(self):
        print 'Abstract2'

class Concrete(models.Model):
    _inherit = 'openacademy.abstract'
    _name = 'openacademy.concrete'

class SchedulerDemo(models.TransientModel):
    _name = 'openacademy.scheduler_demo'

    # This function is called when the scheduler goes off
    def process_demo_scheduler_queue(self):
        scheduler_line_obj = self.env['scheduler.demo']

        # Contains all ids for the model scheduler.demo\
        scheduler_line_ids = self.env['scheduler.demo'].search([])
        # Loops over every record in the model scheduler.demo
        for scheduler_line_id in scheduler_line_ids:
            # Contains all details from the record in the variable scheduler_line
            scheduler_line = scheduler_line_obj.browse(scheduler_line_id.id)
            numberOfUpdates = scheduler_line.numberOfUpdates
            # Prints out the name of every record.
            _logger.info('line: ' + scheduler_line.name)

            # Update the record
            scheduler_line.write({'numberOfUpdates': (numberOfUpdates + 1), 'lastModified': datetime.date.today()})

    @api.model
    def automated_action_method(self):
        active_ids = self._context.get('active_ids')
        print 'Automated Action: automated_action_method '
        for active_id in active_ids:
            self.env['openacademy.course'].browse(active_id).name = 'name'

        return True

    @api.model
    def custom_funct_date(self):
        # print "make sure that this action is called from th server action "
        # compute you date
        import time

        tree_id = self.env.ref("openacademy.course_tree_view")
        form_id = self.env.ref("openacademy.course_form_view")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Courses',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'openacademy.course',
            # 'domain': [('date_order', '>=', my_date)],
            # 'domain': [('create_date', '>=', time.strftime('%Y-%m-%d 00:00:00')),('create_date', '<', time.strftime('%Y-%m-%d 23:59:59'))],
            'domain': [('create_date', '>', (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))],
            'views': [(tree_id.id, 'tree'), (form_id.id, 'form')],
            'target': 'current',
            'context': None,
        }