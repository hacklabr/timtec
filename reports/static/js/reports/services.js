
(function (angular) {
    'use strict';
    /* Services */
    angular.module('reports.services', ['ngResource']).
        factory('CourseUserReport', function($resource){
            return $resource('/api/reports', {}, {
            });
        }).factory('CourseStats', function($resource){
            return $resource('/api/course_stats/:courseId', {}, {
            });
        });
})(angular);
