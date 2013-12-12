(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.filter('capfirst', function() {
        return function(text) {
            if ( text && text.constructor === String && text.length > 0 ) {
                return text.charAt(0).toUpperCase() + text.substring(1);
            }
            return '';
        };
    });

})(window.angular);