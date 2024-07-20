odoo.define('crm.custom_statusbar', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    var Statusbar = require('web.StatusBar');

    Statusbar.include({
        _onClick: function (event) {
            var self = this;
            var $target = $(event.currentTarget);

            // Check if the clicked field has the 'confirm' class
            if ($target.hasClass('o_statusbar_confirm')) {
                event.preventDefault();

                var message = _t("Are you sure you want to change the status?");
                var confirm = new Promise(function (resolve) {
                    var options = {
                        confirm_callback: resolve,
                    };
                    self.trigger_up('show_dialog', { message: message, options: options });
                });

                confirm.then(function () {
                    self._super.apply(self, arguments);
                });
            }
            else {
                this._super.apply(this, arguments);
            }
        },
    });

});
