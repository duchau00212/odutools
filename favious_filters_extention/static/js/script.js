odoo.define('favious_filters_extention.FavoriteMenu', function (require) {
"use strict";
	var core = require('web.core');
	var Base_FavoriteMenu = require('web.FavoriteMenu');
 
	return Base_FavoriteMenu.extend({ 
		template: 'favious_filters_extention.FavoriteMenu_extention',
		    /**
		     * Creates a $filter JQuery node, adds it to the $filters dict and appends it to the filter menu
		     * @param {Object} [filter] the filter description
		     */
		    append_filter: function (filter) {
		        var self = this;
		        var key = this.key_for(filter);
		        this.$divider = this.$('.divider');
		        //this.$divider.show();
		        if (!(key in this.$filters)) {
		            var $filter = $('<li>')
		                .addClass(filter.user_id ? 'favious-private'
		                                         : 'favious-public')
		                .append($('<a >', {
		                	 'data-toggle': "tab",
		                	 'disable_anchor': true,
		                	 'role': "tab", 
		                	'href': '#'}).html( "<span class='fa fa-filter'> " +  filter.name +"</span>"  ))
		                .insertBefore(this.$divider);
		            this.$filters[key] = $filter;
		        }
		        this.$filters[key].unbind('click').click(function () {
		            self.toggle_filter(filter);
		        });
		    },
	}); 

});

odoo.define('SearchView_extention', function (require) {
	'use strict';
	var favious_filters_extention = require('favious_filters_extention.FavoriteMenu');
	var web_SearchView = require('web.SearchView');
	
	web_SearchView.include({
		initx: function(parent, options) {
	        this.favious_filters_extention = undefined;
	        this.ViewManager = parent;
	        return this._super(parent, options); 
	    },
	   
	    start: function(){
	    	var self = this;
	        this._super(); 
	        var extention_menu = new favious_filters_extention(this, this.query, this.dataset.model, this.action_id, this.favorite_filters);
	        extention_menu.insertAfter(".o_control_panel" );
	        this.ViewManager.on("switch_mode", this, function(n_mode) {
	        	if (n_mode === "form") {
	        		$('.faviours_public_extention').addClass('hidden');
                }
	        	else{
	        		$('.faviours_public_extention').removeClass('hidden');
	        	}
	        });
	    },
	    
	});

});
