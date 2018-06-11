# -*- coding: utf-8 -*-
from odoo import api, http, SUPERUSER_ID, _
import logging


_logger = logging.getLogger(__name__)

# db = 'dev'
# cr = odoo.registry(db).cursor()
# env = api.Environment(cr, SUPERUSER_ID, {})

class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teacher']
        return http.request.render('openacademy.index', {
            # 'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
            'teachers': Teachers.search([])
        })

    @http.route('/openacademy/<name>/', auth='public', website=True)
    def teacher(self, name):
        return '<h1>{}</h1>'.format(name)

    @http.route('/openacademy/<int:id>/', auth='public', website=True)
    def teacher(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    @http.route('/openacademy/<model("openacademy.teacher"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })

    # @http.route('/openacademy/teachers1/', auth='public', website=True)
    # def teacher1(self, **kw):
    #     # env['openacademy.teacher'].getAllTeacher1()
    #     return ''