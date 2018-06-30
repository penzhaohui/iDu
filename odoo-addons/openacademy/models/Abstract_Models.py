# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
import logging
import datetime

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
        for active_id in active_ids:
            self.env['model.name'].browse(active_id).name = 'name'

        return True