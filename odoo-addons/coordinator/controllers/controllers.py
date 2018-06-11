# -*- coding: utf-8 -*-
from odoo import http

# class Coordinator(http.Controller):
#     @http.route('/coordinator/coordinator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/coordinator/coordinator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('coordinator.listing', {
#             'root': '/coordinator/coordinator',
#             'objects': http.request.env['coordinator.coordinator'].search([]),
#         })

#     @http.route('/coordinator/coordinator/objects/<model("coordinator.coordinator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coordinator.object', {
#             'object': obj
#         })