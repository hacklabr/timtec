(function(angular) {
    'use strict';

    var app = angular.module('directive.contenteditable', []);

    app.directive('contenteditable', function(){
        return {
            'restrict': 'A',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {
                if(!ngModel)
                    return;

                ngModel.$render = function(){
                    element.html(ngModel.$viewValue || '');
                };

                element.on('keyup keydown', function(evt) {
                    if( (evt.keyCode || evt.which) === 13 ) {
                        evt.preventDefault();
                        return false;
                    }
                });

                element.on('blur keyup change', function() {
                    scope.$apply(read);
                });

                function read() {
                    var html = element.html();
                    if( attrs.stripBr && html.match(/ *<br\/?> */) ){
                        html = '';
                    }
                    ngModel.$setViewValue(html);
                }
            }
        };
    });
})(window.angular);