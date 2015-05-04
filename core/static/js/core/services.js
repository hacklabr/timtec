(function(angular){
    'use strict';

    var app = angular.module('core.services', []);

    app.factory('Course', function($resource){
        return $resource('/api/course/:courseId', {}, {
            update: {method: 'PUT'}
        });
    });

    app.factory('CarouselCourse', function($resource){
        return $resource('/api/course_carousel/:courseId', {}, {
        });
    });

    app.factory('FlatPage', function($resource){
        return $resource('/api/flatpage/:flatpageId', {}, {
            update: {method: 'PUT'}
        });
    });

    app.factory('Twitter', function($resource){
        return $resource('/api/twitter/', {}, {
        });
    });

})(angular);
