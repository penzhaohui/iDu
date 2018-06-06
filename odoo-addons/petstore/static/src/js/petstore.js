// odoo.define('petstore.petstore', function (require) {
// "use strict";
//     var Class = require('web.Class');
//     var AbstractAction = require('web.AbstractAction');
//     var AbstractField = require('web.AbstractField');
//     var Widget = require('web.Widget');
//     var core = require('web.core');
//     var utils = require('web.utils');
//     var rpc = require('web.rpc');
//
//     var _t = core._t;
//     var _lt = core._lt;
//
//     // widget to display last record name of the oepetstore.message_of_the_day
//     var MessageOfTheDay = AbstractAction.extend({
//         template: "MessageOfTheDay",
//         start: function () {
//             var self = this;
//             return self._rpc({ model: "petstore.message_of_the_day", method: "my_method" }).then(function (result) {
//                 self.$(".oe_mywidget_message_of_the_day").text(result);
//             });
//         },
//     });
//
//     var PetToysList = AbstractAction.extend({
//         template: 'PetToysList',
//         events: {
//             'click .oe_petstore_pettoy': 'selected_item',
//         },
//         start: function () {
//             var self = this;
//             return self._rpc({ model: "product.product", method: "my_method" }).then(function (results) {
//                 // display last all items in the product.product
//                 var i=1;
//                 _.each(results,function(item){
//                     console.log();
//                     console.log(item['display_name'])
//                     self.$el.append(QWeb.render('PetToy', {
//                         item: {
//                             "name": item['display_name'] , "image": item['image']}}));
//                 })
//             });
//         },
//         selected_item: function (event) {
//             this.do_action({
//                 type: 'ir.actions.act_window',
//                 res_model: 'product.product',
//                 res_id: $(event.currentTarget).data('id'),
//                 views: [[false, 'form']],
//             });
//         },
//     });
//
//     var HomePage = AbstractAction.extend({
//         template : "HomePage",
//         start: function () {
//             var self = this;
//              self._rpc({model : "petstore.message_of_the_day", method : "my_method", args : ""}).then(function(result){
//                  self.$el.append("<div>Hello " + result + "</div>");
//              });
//
//              return $.when(
//                 new PetToysList(this).appendTo(this.$('.oe_petstore_homepage_left')),
//                 new MessageOfTheDay(this).appendTo(this.$('.oe_petstore_homepage_right'))
//             );
//
//         },
//
//         color_changed : function(){
//             console.log(this.colorInput.get("color"));
//             self.$(".oe_color_div").css("background-color", this.colorInput.get("color"));
//
//         }
//     });
//
//     /*
//     var HomePage = Widget.extend({
//         init: function(parent) {
//             this._super(parent);
//             console.log("Hello JS, I'm inside of init.");
//         },
//         start: function() {
//             console.log("Your pet store home page loaded");
//         },
//     });
//     */
//     core.action_registry.add('petstore.homepage', HomePage);
// });

odoo.define('petstore.petstore', function (require) {
    "use strict";
    var Class = require('web.Class');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var utils = require('web.utils');
    var web_client = require('web.web_client');
    var data = require('web.data');
    // var AbstractAction = require('web.AbstractAction');
    // var ControlPanelMixin = require('web.ControlPanelMixin');

    // var MessageOfTheDay = Widget.extend({
    //     template: "MessageOfTheDay",
    //     start: function() {
    //         var self = this;
    //         return new instance.web.Model("petstore.message_of_the_day")
    //             .query(["message"])
    //             .order_by('-create_date', '-id')
    //             .first()
    //             .then(function(result) {
    //                 self.$(".oe_mywidget_message_of_the_day").text(result.message);
    //             });
    //     },
    // });

    //var rpc = require('web.rpc');
    var MessageOfTheDay = Widget.extend({
        template: "MessageOfTheDay",
        start: function() {
            // rpc.query({
            //       // your model
            //       model: 'petstore.message_of_the_day',
            //       //read data or another function
            //       method: 'my_method',
            //       //args, first id of record, and array another args
            //       args: [],
            //      })
            //      .then(function(result){
            //         //your code when data read
            //        self.$(".oe_mywidget_message_of_the_day").text(result[0]);
            //       });
             var message_of_the_day = new Model('petstore.message_of_the_day');
             message_of_the_day.call("my_method",{context: new data.CompoundContext({'key':'input_key','value': 'input_value',})})
                .then(function (result) {
                    self.$(".oe_mywidget_message_of_the_day").text(result[0]);
                });
        },
    });

    // var HomePage = AbstractAction.extend(ControlPanelMixin, {
    //     template: "HomePage",
    //     start: function() {
    //         var messageofday = new MessageOfTheDay(this);
    //         messageofday.appendTo(this.$el);
    //     },
    // });

    var HomePage = Widget.extend({
        init: function(parent) {
            this._super(parent);
            console.log("Hello JS, I'm inside of init.");
        },
        start: function() {
            console.log("Your pet store home page loaded");
            var messageofday = new MessageOfTheDay(this);
            messageofday.appendTo(this.$el);
        },
    });

    core.action_registry.add('petstore.homepage', HomePage);

})
// https://stackoverflow.com/questions/47758347/odoo-10-javascript-widget-not-working-could-not-find-client-action-petstore-ho
// https://stackoverflow.com/questions/49870183/how-to-call-python-function-in-odoo11-js-file