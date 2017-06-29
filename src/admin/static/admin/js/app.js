'use strict';

import jQuery from 'jquery';
global.jQuery = jQuery;
global.$ = global.jQuery;

import 'uikit';
import 'uikit/dist/js/components/datepicker.min';
import 'uikit/dist/js/components/sortable.min';

import textile from 'textile-js';
global.textile = textile;

$(function() {
    var yustina = new Yustina();
    yustina.bindTextile();
})

function Yustina() {
    var self = this;
};

Yustina.prototype.bindTextile = function() {
    var max_delay = 3000;
    var processing_time = 0;
    var component = $('[data-textile]');

    $.each(component, function(idx, cmp) {
        var tx_input = $('textarea', cmp);
        var input = tx_input[0];
        var text_preview = $('.js-textile_preview', cmp)[0];
        var last = null;

        function convert_text(newval) {
            if (arguments.length === 1 && typeof newval === 'string') {
                input.value = newval;
            }
            var text = tx_input.val();
            if (text && text == last) { return; }
            last = text;
            var html = textile.convert(text);
            text_preview.innerHTML = html;
        }
        var convertTextTimer;
        function on_input(e) {
            clearTimeout(e);
            var defer_time = Math.min(processing_time, max_delay);
            convertTextTimer = setTimeout(convert_text, defer_time);
        }
        $(tx_input).on('keyup', on_input).focus();
        convert_text($(tx_input).val());
    });
};
