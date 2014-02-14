
(function (angular) {
    'use strict';
    /* Services */
    angular.module('reports.services', ['ngResource']).
        factory('CourseUserReport', function($resource){
            return $resource('/api/reports', {}, {
            });
        });
})(angular);
