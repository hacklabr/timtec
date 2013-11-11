'use strict';

/* Services */
    
angular.module('courseMaterial.services', ['ngRoute', 'ngResource']).
    factory('CourseMaterial', function($resource){
        return $resource('/api/course_material/:course/', {}, {
            update: {method: 'PUT'},
        });
    }).
    factory('Course', function($resource){
        return $resource('/api/course/:course_slug/',{});
    });

