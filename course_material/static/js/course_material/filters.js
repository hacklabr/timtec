(function (angular) {
    'use strict';

    var app = angular.module('courseMaterial.filters', []);

    app.filter('filename', function() {
        return function(input) {
            // do some bounds checking here to ensure it has that index
            var path_array = input.split('/');
            return path_array[path_array.length - 1];
        };
    });

})(angular);
