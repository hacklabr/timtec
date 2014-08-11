(function($){
    'use strict';

    var oldMax = 0;
    var oldVisible = 0;
    var oldWindowWidth = 0;

    function res () {
        var $visibleFull = $('.js-fullheight:visible');
        var visible = $visibleFull.length;
        if(visible <= 0)
            return;

        var heights = $visibleFull.map(function () {
            return $(this).height();
        }).get();
        var lefts = $visibleFull.map(function () {
            return $(this).offset().left;
        }).get();
        var footerpos = $('.main-footer').offset().top - $visibleFull.offset().top;
        heights.push(footerpos);
        var tallerSize = Math.max.apply(null, heights);

        // cache: only run if things changed since last time
        if((oldMax === tallerSize) &&
           (oldVisible === visible) &&
           (oldWindowWidth === $(window).width())) {
            return;
        } else {
            oldMax = tallerSize;
            oldVisible = visible;
            oldWindowWidth = $(window).width();
        }

        // console.log('v', oldVisible, 't', oldMax, 'f', footerpos);

        function positionBack (sel1, sel2, makeTall) {
            var $b1 = $(sel1);
            var $c1 = $(sel2 + ':visible');
            if($c1.length > 0) {
                $b1.show();
                if(makeTall)
                    $b1.height(tallerSize);
                else
                    $b1.height($c1.outerHeight());
                $b1.width($c1.outerWidth());
                $b1.offset($c1.offset());
            } else {
                $b1.hide();
            }
        }

        var makeTall = true;
        if((oldVisible == 2) && (lefts[0] === lefts[1]))
            makeTall = false;
        // console.log('mt', makeTall);
        positionBack('.b1', '.c1', makeTall);
        positionBack('.b2', '.c2', makeTall);
    }

    window.timtec_res = res;

    $(function () {
        res();
        $(window).resize(res);
        // $(document).bind('DOMSubtreeModified', res);
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
