(function(angular) {
    'use strict';

    var app = angular.module('directives.layout', []);

    app.directive('ngLessonFullheight', ['$window', function($window) {
        return {
            'restrict': 'A',
            'scope': {
                        'whatched_element': '@whatchedElement'
            },
            'link': function(scope, el) {

                function full_height() {
                    var course_content_height = angular.element('#course-content').outerHeight();
                    var lesson_header_height = angular.element('#lesson-header').outerHeight();
                    var footer_margin_top = parseInt(angular.element('#main-footer').css('marginTop'), 10);
                    el.css('margin-top', -1*lesson_header_height);
                    el.css('padding-top', lesson_header_height);
                    el.css('height', (course_content_height+footer_margin_top));
                    el.css('margin-bottom', -1*(course_content_height+footer_margin_top));
                }

                scope.$watch(function() {
                    if (angular.element('body').width() > 980) {
                        full_height();
                    }
                });

                angular.element($window).bind('resize', function() {
                    if (angular.element('body').width() <= 980) {
                        el.css('margin-top', '');
                        el.css('padding-top', '');
                        el.css('height', '');
                        el.css('margin-bottom', '');
                    } else {
                        full_height();
                    }
                });
            }
        };
    }]);
})(window.angular);
