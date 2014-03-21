(function(angular){
    'use strict';

    var app = angular.module('core.services', []);

    app.factory('Course', function($resource){
        return $resource('/api/course/:courseId', {}, {
        });
    });

})(angular);
