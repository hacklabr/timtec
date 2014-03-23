(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course',
        function ($scope, Course) {
            $scope.courses = Course.query({'home_published': 'True'}, function(courses) {
                if (courses.length > 6) {
                    $scope.courses = courses.slice(0,6);
                }
            });

            $scope.upcoming_courses = Course.query({'home_published': 'False'}, function(upcoming_courses) {
                if (upcoming_courses.length > 3) {
                    $scope.upcoming_courses = upcoming_courses.slice(0,3);
                }
            });
        }
    ]);

})(angular);
