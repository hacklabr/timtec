(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.controller('CourseListController', [
        '$scope', 'Course',
        function ($scope, Course) {
            $scope.courseList = [];

            Course.query(function(list){
                $scope.courseList = list;
            });
        }
    ]);
})(window.angular);