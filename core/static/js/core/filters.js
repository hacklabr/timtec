(function(angular){
    'use strict';

    var app = angular.module('core.filters', []);

    app.filter('capitalize', function() {
        return function(input, scope) {
            if (input!==null)
                return input.substring(0,1).toUpperCase()+input.substring(1);
        };
    });

})(angular);
