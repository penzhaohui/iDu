# -*- coding: utf-8 -*-
from odoo import models, fields
import xlrd, base64

class Region(models.Model):
    _name = "openacademy.region"

    xls = fields.Binary('XLS File')

    def btn_import(self, cr, uid, ids, context=None):
        return