(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course', 'CarouselCourse', 'Twitter', function ($scope, Course, CarouselCourse, Twitter) {

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
            if (row.length > 0) {
                $scope.courses_rows.push(row);
            }
        });

        $scope.all_courses = Course.query({'public_courses': 'True'}, function(all_courses) {

        });

        $scope.selectCourse = function(course) {
            course.home_published = !course.home_published;
            course.toBeSaved = true;
        };

        $scope.saveCourses = function(course) {
            var homeCourses = [];
            angular.forEach($scope.all_courses, function(course) {
                if (course.home_published) {
                    homeCourses.push(course);
                }
                if (course.toBeSaved) {
                    course.$update({courseId: course.id});
                }
            });
            homeCourses.sort(compare_by_position);
            $scope.courses = homeCourses;
        };

        $scope.upcoming_courses = CarouselCourse.query({'home_published': 'False'}, function(upcoming_courses) {

            $scope.upcoming_courses_rows_3 = [];

            for (var i = 0; i < upcoming_courses.length; i++) {
                var row = [];
                row[0] = $scope.upcoming_courses[i];

                if (upcoming_courses.length - i > 1){
                    // normal case
                    row[1] = $scope.upcoming_courses[i+1];
                    if (upcoming_courses.length - i > 2)
                        row[2] = $scope.upcoming_courses[i+2];
                    else
                        row[2] = $scope.upcoming_courses[upcoming_courses.length - i - 2];
                } else {
                    row[1] = $scope.upcoming_courses[upcoming_courses.length - i - 1];
                    row[2] = $scope.upcoming_courses[upcoming_courses.length - i];
                }
                $scope.upcoming_courses_rows_3.push(row);
            }
        });

        $scope.twits = Twitter.query({});
    }]);

})(angular);

