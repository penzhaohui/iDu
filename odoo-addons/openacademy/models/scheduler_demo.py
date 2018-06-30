# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
import datetime

_logger = logging.getLogger(__name__)

# https://www.odoo.yenthevg.com/creating-automated-actions-in-odoo/
class scheduler_demo(models.Model):
    _name = 'scheduler.demo'
    name = fields.Char(required=True)
    numberOfUpdates = fields.Integer('Number of updates', help='The number of times the scheduler has run and updated this field')
    lastModified = fields.Date('Last updated')
