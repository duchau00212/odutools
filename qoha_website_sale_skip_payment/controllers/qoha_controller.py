# -*- coding: utf-8 -*-
import json
import logging 

from odoo import http, tools, _
from odoo.http import request  
from odoo.addons.website_sale.controllers.main import WebsiteSale 
from werkzeug.exceptions import Forbidden
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
        acquirer_id = request.env.ref("payment.payment_acquirer_custom")# 9
        tx_values = {
                'acquirer_id': acquirer_id.id,
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
            'payment_acquirer_id': acquirer_id.id,
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
        search_ids = request.env['mail.followers'].sudo().search( [('partner_id', '=',order.partner_id.id),
                                                                   ('res_id', '=', order.id),
                                                                   ('res_model', '=', "sale.order")
                                                                    ], limit = 1  )
        if not search_ids:
            request.env['mail.followers'].sudo().create( {'partner_id': order.partner_id.id,
                                                      'res_id': order.id,
                                                      'res_model': "sale.order",
                                                      })

        #call to payment
        request.website.sale_reset()
        return request.redirect("/shop/confirmation")
    
    
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post): 
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order) 
        if post:
            values = self.checkout_values(**post)
            # Avoid useless rendering if called in ajax
            if post.get('xhr'):
                return 'ok'
            return request.render("website_sale.checkout", values)
        return request.redirect('/shop/address') 

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order(force_create=1)
        mode = ('new', 'shipping')
        def_country_id = order.partner_id.country_id
        values, errors = {}, {}

        partner_id = request.env.user.partner_id.id #int(kw.get('partner_id', request.website.partner_id.id ))

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ('new', 'billing')
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                def_country_id = request.env['res.country'].search([('code', '=', country_code)], limit=1)
            else:
                def_country_id = request.website.user_id.sudo().country_id
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ('new', 'shipping')
            else: # no mode - refresh without post?
                return request.redirect('/shop/checkout')
        
        # IF POSTED
        if 'submitted' in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)

                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.onchange_partner_id()
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/qoha_shop/confirm_order')

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        country = country and country.exists() or def_country_id
        render_values = {
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'country': country,
            'countries': country.get_website_sale_countries(mode=mode[1]),
            "states": country.get_website_sale_states(mode=mode[1]),
            'error': errors,
            'callback': kw.get('callback'),
        }
        return request.render("website_sale.address", render_values)

    
    
qoha_shop()