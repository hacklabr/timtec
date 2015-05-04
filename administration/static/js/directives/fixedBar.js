(function(angular) {
    'use strict';

    var app = angular.module('directive.fixedBar', []);

    app.directive('fixedBar', function() {
        return {
            'restrict': 'A',
            'link': function(scope, el) {
                var parent = el.parent();

                var barOffsetTop = el.offset().top;
                var barHeight = parseInt(el.css('height'), 10);
                var barMarginTop = parseInt(el.css('marginTop'), 10);
                var barAbsMarginTop = Math.abs(barMarginTop);

                var preparedHeight = barHeight + barAbsMarginTop + 'px';
                var preparedTop = barAbsMarginTop + 'px';

                window.onscroll = function() {
                    if (window.scrollY >= barOffsetTop) {
                        parent.css('margin-top', preparedHeight);
                        el.css('top', preparedTop);
                        el.addClass('actions-menu-scroll');
                    } else {
                        parent.css('margin-top', '');
                        el.css('top', '');
                        el.removeClass('actions-menu-scroll');
                    }
                };
            }
        };
    });
})(window.angular);
