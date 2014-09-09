(function(angular){
    'use strict';

    var app = angular.module('core.services', []);

    app.factory('Course', function($resource){
        return $resource('/api/course/:courseId', {}, {
        });
    });

    app.factory('CarouselCourse', function($resource){
        return $resource('/api/course_carousel/:courseId', {}, {
        });
    });

    app.factory('Twitter', function($resource){
        return $resource('/api/twitter/', {}, {
        });
    });

})(angular);
