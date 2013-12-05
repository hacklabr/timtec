(function(angular){
    'use strict';
    var app = angular.module('new-course');

    app.factory('Course', ['$resource', function($resource) {
        var Course = $resource('/api/course/:slug', {'slug':'@slug'});
        return Course;
    }]);

})(window.angular);