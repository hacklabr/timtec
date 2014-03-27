(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course', 'Twitter', function ($scope, Course, Twitter) {

        function compare_by_position(a,b) {
            if (a.home_position < b.home_position)
               return -1;
            if (a.home_position > b.home_position)
               return 1;
            return 0;
        }

        $scope.courses = Course.query({'home_published': 'True'}, function(courses) {

            courses.sort(compare_by_position);
            $scope.courses_rows = [];
            var row = [];
            var index = 0;
            angular.forEach(courses, function(course) {
                row.push(course);
                if (index == 1) {
                    $scope.courses_rows.push(row);
                    row = [];
                    index = 0;
                } else
                    index++;
            });
        });

        $scope.upcoming_courses = Course.query({'home_published': 'False'}, function(upcoming_courses) {
            if (upcoming_courses.length > 3) {
                $scope.upcoming_courses = upcoming_courses.slice(0,3);
            }
        });

        $scope.twits = Twitter.query({});
    }]);

})(angular);
