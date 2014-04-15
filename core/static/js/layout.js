(function($){
    'use strict';

    var oldHeight;
    function res () {
        if($(window).width() < 992) {
            console.log('nao rodei');
            return
        } else {
            console.log($(window).width());
        }
        var footerpos = $('.main-footer').position().top  -  $('header.main-header').outerHeight(true);
        $('.js-fullheight').each(function () {
            var $this = $(this);

            $(this).height(Math.max($(this).height(), this.scrollHeight));
            $this.height(footerpos - $this.position().top);
            // console.log($this.attr('class'), $this.height(), $this.innerHeight(), this.scrollHeight, $this.outerHeight());
        });

        oldHeight = $('.main-footer').position().top;
    }

    $(function () {
        // res();
        // $(window).resize(res);
        // $(document).bind('DOMSubtreeModified', res);
        // setTimeout(res, 500);
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
