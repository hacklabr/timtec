(function($){
    'use strict';

    function fullHeight(element) {
        var height = $('.wrapper').height();
        if ($('.wrapper').width() > 992) {
            $(element).height(height);
        }
    }

    $(function () {
        fullHeight('.js-fullheight');
    });

})(window.jQuery);
