# -*- coding: utf-8 -*-
# from odoo import http


# class KokaiQc(http.Controller):
#     @http.route('/kokai_qc/kokai_qc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kokai_qc/kokai_qc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kokai_qc.listing', {
#             'root': '/kokai_qc/kokai_qc',
#             'objects': http.request.env['kokai_qc.kokai_qc'].search([]),
#         })

#     @http.route('/kokai_qc/kokai_qc/objects/<model("kokai_qc.kokai_qc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kokai_qc.object', {
#             'object': obj
#         })
