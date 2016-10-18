# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, tools

class res_country( models.Model ):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        return self.sudo().search([ ('name', 'like', 'Vietnam%') ])

    def get_website_sale_states(self, mode='billing'):
        return self.sudo().state_ids

