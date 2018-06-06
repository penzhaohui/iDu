odoo.define('openacademy.tree_view_button', function (require){
"use strict";

var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;


ListView.include({

        render_buttons: function($node) {
                console.log("Debug for tree_view_button")
                var self = this;
                this._super($node);
                this.$buttons.find('.o_list_tender_button_create').click(this.proxy('tree_view_action'));
        },

        tree_view_action: function () {
            console.log("Debug for tree_view_button.do_action")
            this.do_action({
                    type: "ir.actions.act_window",
                    name: "course",
                    res_model: "openacademy.course",
                    views: [[false,'form']],
                    target: 'current',
                    view_type : 'form',
                    view_mode : 'form',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
            });
            return { 'type': 'ir.actions.client','tag': 'reload', }
        }
});

});