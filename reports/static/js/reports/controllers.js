
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('CourseUsersReportsCtrl', ['$scope', '$window', '$location', 'CourseUserReport',
            function ($scope, $window, $location, CourseUserReport) {
                $scope.courseId = /course\/([^\/]+)\/stats/.extract(location.pathname, 1);
                $scope.users_reports = CourseUserReport.query({course: $scope.courseId}, function (users_reports){});
        }]).
        controller('CourseLessonsReportsCtrl', ['$scope', '$window', '$location', 'CourseUserReport', 'CourseStats',
                function ($scope, $window, $location, CourseUserReport, CourseStats) {
                    $scope.courseId = /course\/([^\/]+)\/stats/.extract(location.pathname, 1);
                    $scope.course_stats = CourseStats.get({courseId: $scope.courseId}, function (course_stats){});
        }]);
})(angular);
