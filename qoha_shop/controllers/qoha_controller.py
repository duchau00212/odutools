# -*- coding: utf-8 -*-
import json
import logging 

from odoo import http, tools, _
from odoo.http import request  
from odoo.addons.website_sale.controllers.main import WebsiteSale 
from werkzeug.exceptions import Forbidden
import urllib 

class qoha_shop(WebsiteSale): #(http.Controller):
    
    def hauga  (self):
        print 'Im hauga'
      
qoha_shop()