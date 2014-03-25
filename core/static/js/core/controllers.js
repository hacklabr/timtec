(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course', 'Twitter', function ($scope, Course, Twitter) {
        $scope.courses = Course.query({'home_published': 'True'}, function(courses) {
            if (courses.length > 6) {
                $scope.courses = courses.slice(0,6);
            }
            $scope.courses_rows = [];
            var row = [];
            var index = 0;
            angular.forEach($scope.courses, function(course) {
                row.push(course);
                if (index == 1) {
                    $scope.courses_rows.push(row);
                    row = [];
                    index = 0;
                } else
                    index++;
            });
            var bla = 1;
        });

        $scope.upcoming_courses = Course.query({'home_published': 'False'}, function(upcoming_courses) {
            if (upcoming_courses.length > 3) {
                $scope.upcoming_courses = upcoming_courses.slice(0,3);
            }
        });

        $scope.twits = Twitter.query({});
    }]);

})(angular);
