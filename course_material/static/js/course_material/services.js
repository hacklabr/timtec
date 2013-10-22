'use strict';

/* Services */
    
angular.module('forum.services', ['ngRoute', 'ngResource']).
    factory('CourseMaterialService', function($resource){
        return $resource('/api/course_material/', {}, {
        });
    });

