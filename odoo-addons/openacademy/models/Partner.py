# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)

    city = fields.Many2one('res.city', 'city')
    district = fields.Many2one('res.district', 'district')

    def test_act(self):
        print "Server Action is triggered!!!"
        return True

class ResCity(models.Model):
    _name = 'res.city'

    name = fields.Char('name')
    state = fields.Many2one('res.country.state', 'state')

class ResDistrict(models.Model):
    _name = "res.district"

    name = fields.Char('name')
    city = fields.Many2one('res.city', "city")
