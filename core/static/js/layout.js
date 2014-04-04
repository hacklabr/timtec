(function($){
    'use strict';

    function fullHeight(element, extra) {
        if(!extra) extra = 0;
        var height = ($(window).height() - ($('.main-header').height() + extra + $('.main-footer').height()));
        if ($(window).height() > 768 || extra === 0) {
            $(element).height(height);
        }
    }

    function resizes () {
        console.log('rere');
        fullHeight('.js-fullheight');
        fullHeight('.js-fullheight-container', 85);
    }

    $(function () {
        resizes();
        $(window).resize(resizes);
    });

    $(function () {
        if (window.location.pathname == '/courses') {
            $('#courses-tab').addClass('active');
        } else if (window.location.pathname == '/pages/about/') {
            $('#about-tab').addClass('active');
        } else if (window.location.pathname == '/pages/institute/') {
            $('#institute-tab').addClass('active');
        }
    });

})(window.jQuery);
