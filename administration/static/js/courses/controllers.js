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
                all: false,
                published : true,
                listed : true,
                draft : true,
                textsearch: '',
                isValid : function(course){
                    return (
                        $scope.filters.all || ($scope.filters[course.status])
                    ) && (
                        !$scope.filters.textsearch ||
                        course.name.toLowerCase().indexOf($scope.filters.textsearch.toLowerCase()) >= 0
                    );
                }
            };

            Course.query(function(list){
                $scope.courseList = list;
            });
        }
    ]);
})(window.angular);