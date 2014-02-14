
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('CourseReportsCtrl', ['$scope', '$window', '$location', 'CourseUserReport',
            function ($scope, $window, $location, CourseUserReport) {
                $scope.courseId = /course\/([^\/]+)\/stats/.extract(location.pathname, 1);
                $scope.users_reports = CourseUserReport.query({course: $scope.courseId}, function (users_reports){});
    }]);
})(angular);
