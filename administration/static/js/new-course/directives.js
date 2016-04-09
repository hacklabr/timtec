(function(angular){
    'use strict';
    var app = angular.module('new-course.directives', []);

    app.directive('file', function(){
        return {
            'restrict': 'AE',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {

                if (element.context.tagName == 'INPUT'){
                    element.attr('type', 'file');

                    element.bind("change", function (changeEvent) {
                        scope.$apply(function () {
                            ngModel.$setViewValue(changeEvent.target.files[0]);
                        });
                    });
                } else {
                    var input = document.createElement('input');

                    input.type = 'file';
                    input.onchange = function(evt) {
                        if(evt.target.files) {
                            ngModel.$setViewValue(evt.target.files[0]);
                        }
                        scope.$apply();
                    };

                    for( var att in attrs ) {
                        if(! /^ng/.test(att)) {
                            input[att] = element.attr(att);
                        }
                    }
                    input.className = element.attr('class').replace(/\bng[^ ]+ */g, '').trim();
                    element.attr('class', '');
                    element.removeAttr("id");
                    element.removeAttr("name");
                    element.append(input);
                }
            }
        };
    });

    app.directive('previewImage', function(){
        return {
            'restrict': 'A',
            'link': function(scope, element, attrs) {
                var img = element[0];
                var reader = new FileReader();

                reader.onload = function(evt) {
                    img.src = evt.target.result;
                };

                if( attrs.ngModel ) {
                    scope.$watch(attrs.ngModel, function(d){
                        if( window.File && d && d.constructor === window.File ) {
                            img.style.display = '';
                            reader.readAsDataURL( d );
                        }
                    });
                }
            }
        };
    });

})(window.angular);
