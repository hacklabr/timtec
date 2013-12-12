(function(angular) {
    'use strict';

    var app = angular.module('directive.contenteditable', []);

    app.directive('contenteditable', function(){
        return {
            'restrict': 'A',
            'require': '?ngModel',
            'controller': ['$scope', '$element', '$document', '$attrs',
                function($scope, $element, $document, $attrs){
                    if($attrs.placeholder) {
                        var id = $element[0].nodeName + Math.random().toString(16).substring(2);
                        $element.attr('id', id);
                        var style = $document[0].createElement('style');
                        style.type = 'text/css';
                        style.innerHTML = '#'+id+':empty:before { content: "'+$attrs.placeholder+'";}';
                        $document[0].body.appendChild(style);
                    }
                }
            ],
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

                element.on('keyup change', function() {
                    scope.$apply(read);
                });

                element.on('blur', function(){
                    var text = element.text().trim();
                    element.text(text.trim());
                    scope.$apply(read);
                });

                function read() {
                    var html = element.text();
                    if( attrs.stripBr && html.match(/ *<br\/?> */) ){
                        html = '';
                    }
                    ngModel.$setViewValue(html);
                }
            }
        };
    });
})(window.angular);