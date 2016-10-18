# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.website.models.website import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm

_logger = logging.getLogger(__name__)

class add_product_to_cart_by_ajax(http.Controller):

    @http.route(['/shop/ajax/cart/update_json'], type='json', auth="public", methods=['POST', 'GET'], website=True, csrf=False)
    def ajax_cart_update_json(self, product_id, add_qty=1, set_qty=0, **kw):
        request.website.sale_get_order(force_create=1)._cart_update(
            product_id=int(product_id),
            add_qty=float(add_qty),
            set_qty=float(set_qty),
        )
        order = request.website.sale_get_order(force_create=1)
        return {'cart_quantity': order.cart_quantity}
    
    