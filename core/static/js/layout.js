(function($){
    'use strict';

    var oldHeight;
    function res () {
        if($('.js-fullheight').height() !== oldHeight) {
            $('.js-fullheight').height($('.main-footer').position().top - 80);
        }
        oldHeight = $('.js-fullheight').height();
        console.log('vai');
    }

    $(function () {
    //     resizes();
        res();
        $(window).resize(res);
        $(document).bind('DOMSubtreeModified', res);
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
