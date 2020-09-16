# -*- coding: utf-8 -*-
# from odoo import http


# class Workshop(http.Controller):
#     @http.route('/workshop/workshop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/workshop/workshop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('workshop.listing', {
#             'root': '/workshop/workshop',
#             'objects': http.request.env['workshop.workshop'].search([]),
#         })

#     @http.route('/workshop/workshop/objects/<model("workshop.workshop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('workshop.object', {
#             'object': obj
#         })
