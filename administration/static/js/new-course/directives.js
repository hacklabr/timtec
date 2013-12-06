(function(angular) {
    'use strict';

    var app = angular.module('new-course');

    app.directive('warning', function(){
        var template = ''+
            '<span class="label label-danger pull-right"'+
            '      data-toggle="tooltip" ng-show="model" title="{{model.toString()}}">'+
            '    <i class="fa fa-warning"></i>'+
            '</span>';

        return {
            'restrict': 'E',
            'template': template,
            'scope': {
                'model': '='
            },
            'link': function(scope, element) {
                if(window.jQuery && window.jQuery.fn.tooltip) {
                    var el = element.find('[data-toggle=tooltip]');
                    scope.$watch('model', function(){
                        if(!scope.model)
                            return;

                        el.tooltip('show');
                        setTimeout(function(){
                            el.tooltip('hide');
                        }, 2000);
                    });
                }
            }
        };
    });


})(window.angular);