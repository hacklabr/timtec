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

    app.filter("nullToEnd", function () {
        return function (array, key, invert) {
            if (!angular.isArray(array)) return;
            var present = array.filter(function (item) {
                return item[key];
            });
            var empty = array.filter(function (item) {
                return !item[key];
            });
            if (invert)
                return empty.concat(present);
            else
                return present.concat(empty);
        };
    });

})(window.angular);