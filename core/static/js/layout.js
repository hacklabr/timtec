(function($){
    'use strict';

    function res () {
        var $visibleFull = $('.js-fullheight:visible');
        var heights = $visibleFull.map(function () {
            return $(this).height();
        }).get();

        var footerpos = $('.main-footer').offset().top  -  $('header.main-header').height() + 5; // Discover where does this 5 pixels come from
        heights.push(footerpos);
        var tallerSize = Math.max.apply(null, heights);

        console.log($visibleFull.length);
        console.log(tallerSize, footerpos);

        function positionBack (sel1, sel2) {
            var $b1 = $(sel1);
            var $c1 = $(sel2 + ':visible');
            if($c1.length > 0) {
                $b1.show();
                $b1.height(tallerSize);
                $b1.width($c1.outerWidth());
                $b1.offset($c1.offset());
            } else {
                $b1.hide();
            }
        }

        positionBack('.b1', '.c1');
        positionBack('.b2', '.c2');
    }

    $(function () {
        res();
        $(window).resize(res);
        $(document).bind('DOMSubtreeModified', res);
        setTimeout(res, 500);
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
