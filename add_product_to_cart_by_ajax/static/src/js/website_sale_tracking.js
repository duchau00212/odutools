odoo.define('add_product_to_cart_by_ajax.tracking', function(require) {
    var ajax = require('web.ajax');
    $(document).ready(function () {
        // Add a product into the cart 
        $(".oe_website_sale form[action='/shop/cart/update'] a.a-submit-ajax").on('click', function(o) {
            var self = $(this);
            self.addClass('hidden');
            var prod_id = self.parent().children("input[name='product_id']").attr('value');
            ajax.jsonRpc("/shop/ajax/cart/update_json", 'call', { 
                'product_id': prod_id,
                'add_qty': 1,
            }).then(function (data) {
                $(".my_cart_quantity").text(data.cart_quantity);
                $("sup.my_cart_quantity").parent().parent().removeClass('hidden');
            });
        });
          
          
          
          
          
          
          
          
          ////////////
          
        $(".oe_website_sale form[action='/shop/cart/update'] a.a-submit-ajax").on('click2', function(o) {
            var self = $(this);
            self.addClass('hidden');
            var prod_id = self.parent().children("input[name='product_id']").attr('value');
            var product_ids = [prod_id]; 
            ajax.jsonRpc("/shop/cart/update_json", 'call', { 
                'product_id': prod_id,
                'add_qty': 1
            }).then(function (data) {
                console.log("Datas::" + JSON.stringify( data) );
                var $q = $(".my_cart_quantity");
                if (data.cart_quantity) {
                    $q.parents('li:first').removeClass("hidden");
                }
                else {
                    $q.parents('li:first').addClass("hidden");
                    $('a[href^="/shop/checkout"]').addClass("hidden");
                }
                $q.html(data.cart_quantity).hide().fadeIn(600);
            }); 
             
        });
          
               
          
          
          
          
          //////////////
          
          
          
          
          
    });
    
});


    