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

    $(function () {
        if (window.location.pathname == '/courses') {
            $('#courses-tab').addClass('active');
        } else if (window.location.pathname == '/about/') {
            $('#about-tab').addClass('active');
        } else if (window.location.pathname == '/institute/') {
            $('#institute-tab').addClass('active');
        }
    });

})(window.jQuery);
