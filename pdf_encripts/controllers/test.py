# -*- coding: utf-8 -*-

from odoo import http, tools, _
from odoo.http import request

class WebsiteSale(http.Controller):

    #@http.route(['/shop/print'], type='http', auth="public", website=True)
    def print_saleorder(self):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            pdf = request.env['report'].sudo().get_pdf_enscript([sale_order_id], 'sale.report_saleorder', 
                                                                data=None, password='hauga' )
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)   )]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')
        
    @http.route(['/shop/print'], type='http', auth="public", website=True)   
    def print_saleorder_test2(self, pwd=False ):
        password=pwd.encode('ascii')
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            pdf = request.env['report'].sudo().with_context({u'password':password }).get_pdf([sale_order_id], 'sale.report_saleorder', data=None )
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)   )]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')
        
        
        
        