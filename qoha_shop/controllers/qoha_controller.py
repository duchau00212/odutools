# -*- coding: utf-8 -*-
import json
import logging 

from odoo import http, tools, _
from odoo.http import request  
from odoo.addons.website_sale.controllers.main import WebsiteSale 
import urllib 

class qoha_shop(WebsiteSale): #(http.Controller):
    
      

    @http.route(['/qoha_shop/confirm_order'], type='http', auth="public", website=True, csrf=False)
    def qoha_shop_confirm_order(self, **post):
        # call to 'shop/confirm_order'   
        order = request.website.sale_get_order()
        order.onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)
        extra_step = request.env.ref('website_sale.extra_info_option')
        
        if extra_step.active:
            return request.redirect("/shop/extra_info")
        
        #payman  
        acquirer_id = 9
        tx_values = {
                'acquirer_id': acquirer_id,
                'type': 'form',
                'amount': order.amount_total,
                'currency_id': order.pricelist_id.currency_id.id,
                'partner_id': order.partner_id.id,
                'partner_country_id': order.partner_id.country_id.id,
                'reference': order.name,
                'sale_order_id': order.id,
                'state': 'pending',
            }
        Transaction = request.env['payment.transaction'].sudo()
        tx = Transaction.create(tx_values)
        request.session['sale_transaction_id'] = tx.id

        # update quotation
        order.write({
            'payment_acquirer_id': acquirer_id,
            'payment_tx_id': request.session['sale_transaction_id'],
            'state': 'sent',
            
        })
        #order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
        post.update(
                    {'currency': order.pricelist_id.currency_id.name, 
                     'amount': order.amount_total, 
                     'reference': order.name, 
                     'return_url': u'/shop/payment/validate'}
                    )
        request.env['payment.transaction'].sudo().form_feedback(post, 'transfer') 
        
        
        
        order.message_partner_ids = [(4, order.partner_id.id, False)] 
        
        request.env['mail.followers'].sudo().create( {'partner_id': order.partner_id.id,
                                                      'res_id': order.id,
                                                      'res_model': "sale.order",
                                                      })

        #call to payment
        request.website.sale_reset()
        return request.redirect("/shop/confirmation")
    
qoha_shop()