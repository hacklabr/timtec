(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.controller('CourseListController', [
        '$scope', 'Course',
        function ($scope, Course) {
            $scope.courseList = [];
            $scope.ordering = 'id';
            $scope.reverse = false;
            $scope.filters = {
                all: true,
                published : true,
                listed : true,
                draft : true,
                check : function(course){
                    return $scope.filters.all || ($scope.filters[course.status]);
                }
            };

            Course.query(function(list){
                $scope.courseList = list;
            });
        }
    ]);
})(window.angular);