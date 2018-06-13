# -*- coding: utf-8 -*-
from odoo import http

# class Leaveapp(http.Controller):
#     @http.route('/leaveapp/leaveapp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/leaveapp/leaveapp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('leaveapp.listing', {
#             'root': '/leaveapp/leaveapp',
#             'objects': http.request.env['leaveapp.leaveapp'].search([]),
#         })

#     @http.route('/leaveapp/leaveapp/objects/<model("leaveapp.leaveapp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('leaveapp.object', {
#             'object': obj
#         })