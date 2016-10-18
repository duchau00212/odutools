# -*- coding: utf-8 -*-
import json
import logging 

from odoo import http, tools, _
from odoo.http import request  
#from odoo.addons.website_sale.controllers.main import WebsiteSale 

class qoha_shop(http.Controller):

    @http.route(['/qoha_shop/confirm_order'], type='http', auth="public", website=True)
    def qoha_shop_confirm_order(self, transaction_id=None, sale_order_id=None,**post):
        # call to 'shop/confirm_order' 
        print "yyyyyyyyyy"
        return "hauga123"
#        #self.confirm_order()
#        order = request.website.sale_get_order()
#        order.onchange_partner_shipping_id()
#        order.order_line._compute_tax_id()
#        request.session['sale_last_order_id'] = order.id
#        request.website.sale_get_order(update_pricelist=True)
#        extra_step = request.env.ref('website_sale.extra_info_option')
#        if extra_step.active:
#            return request.redirect("/shop/extra_info")
#        
#        #call to payment
#        print "MMMMM:", order.id, post
#        return WebsiteSale.payment_validate(transaction_id=transaction_id, sale_order_id=order.id, post)

qoha_shop()