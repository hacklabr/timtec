
(function (angular) {
    'use strict';
    /* Services */
    angular.module('reports.services', ['ngResource']).
        factory('CourseUserReport', function($resource){
            return $resource('/api/reports', {}, {
            });
        }).factory('LessonsUserProgress', function($resource){
            return $resource('/api/lessons_user_progress/:courseId', {}, {
            });
        }).factory('CourseStats', function($resource){
            return $resource('/api/course_stats/:courseId', {}, {
            });
        }).factory('GeneralSummary', function($resource){
            return $resource('/paralapraca/api/summary', {}, {
            });
        }).factory('Contract', function($resource){
            return $resource('/paralapraca/api/contract', {}, {
            });
        });
})(angular);
