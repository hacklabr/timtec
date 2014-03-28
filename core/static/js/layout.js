(function($){
    'use strict';

    function fullHeight(element) {
        var fullHeight = $('.wrapper').height();
        if ($('.wrapper').width() > 992) {
            $(element).height(fullHeight);
        }
    }

    $(function () {
        fullHeight('.js-fullheight');
    });

})(window.jQuery);
