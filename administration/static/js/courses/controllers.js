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
                check : function(course){
                    return true;
                    /* var f = $scope.filters;
                    var search = f.textsearch.toLowerCase();
                    var target = course.name.toLowerCase();

                    return (
                        f.all || f[course.status]
                    ) && (
                        !search || target.match(search)
                    );*/
                }
            };

            Course.query(function(list){
                $scope.courseList = list;
            });
        }
    ]);
})(window.angular);
