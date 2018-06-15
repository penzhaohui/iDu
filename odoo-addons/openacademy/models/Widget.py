# -*- coding: utf-8 -*-
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Widget(models.Model):
    _name = 'openacademy.widget'
    _inherit = ['mail.thread']

    print 'Enter into openacademy.widget'
    _logger.info("Enter into openacademy.widget")

    state = fields.Selection(string='What do you want ?', selection='_get_selection')
    logo = fields.Binary(string="Upload Logo")
    email = fields.Char(string='Widget Email', size=30)
    taxes_id = fields.Many2many('openacademy.course', string='Course')
    date_planned = fields.Datetime(string='Scheduled Date', store=True, index=True)
    progress = fields.Float('Widget Progress', digits=(0, 2))
    url = fields.Char(string='Widget Url', size=30)
    user_domain = fields.Char("User domain", help="Alternative to a list of users")
    category = fields.Selection([
        ('hr', 'Human Resources / Engagement'),
        ('other', 'Settings / Gamification Tools'),
    ], string="Appears in", required=True, default='hr',
        help="Define the visibility of the challenge through menus")

    sequence = fields.Integer(help="Used to order the note stages")
    description = fields.Char('Field Char', size=50)
    description_pad = fields.Char('Pad URL', pad_content_field='description')
    memo = fields.Html('Note Content')

    integer = fields.Integer('Field Integer')
    description = fields.Char('Field Char', size=5)
    text = fields.Text('Field Text')
    date = fields.Date('Field Name')
    dateTime = fields.Datetime('Field Time')

    def _get_selection(self):
        return ([
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('cancel', 'Cancelled'),])
