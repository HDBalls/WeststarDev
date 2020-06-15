# -*- coding: utf-8 -*-
# from odoo import http


# class Bluestar(http.Controller):
#     @http.route('/bluestar/bluestar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bluestar/bluestar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bluestar.listing', {
#             'root': '/bluestar/bluestar',
#             'objects': http.request.env['bluestar.bluestar'].search([]),
#         })

#     @http.route('/bluestar/bluestar/objects/<model("bluestar.bluestar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bluestar.object', {
#             'object': obj
#         })
