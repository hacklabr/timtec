(function($){
    'use strict';

    function fullHeight(element, extra) {
        if(!extra) extra = 0;
        var height = ($('.wrapper').height() - ($('.main-header').height() + extra + $('.main-footer').height()));
        if ($('.wrapper').height() > 780) {
            $(element).height(height);
        }
    }

    $(function () {
        fullHeight('.js-fullheight');
        fullHeight('.js-fullheight-container', 85);
    });

})(window.jQuery);
