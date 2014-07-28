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
                        el.css('left', '0');
                        el.css('position', 'fixed');
                        el.css('right', '0');
                        el.css('top', preparedTop);
                        el.css('z-index', 1000);
                    } else {
                        parent.css('margin-top', '');
                        el.css('position', '');
                        el.css('top', '');
                        el.css('z-index', '');
                    }
                };
            }
        };
    });
})(window.angular);
