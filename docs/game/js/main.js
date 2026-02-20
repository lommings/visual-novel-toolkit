'use strict';
/* global Monogatari */
/* global monogatari */

// 相容性處理
if (typeof Monogatari !== 'undefined' && typeof monogatari !== 'undefined' && monogatari) {
    var $_ready = Monogatari.$_ready || function(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    };

    $_ready(function() {
        monogatari.init('#monogatari');
    });
}
