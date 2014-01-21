(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.controller('CourseListController', [
        '$scope', 'Course', 'Lesson',
        function ($scope, Course, Lesson) {
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
                    var f = $scope.filters;
                    var search = f.textsearch.toLowerCase();
                    var target = course.name.toLowerCase();

                    return (
                        f.all || f[course.status]
                    ) && (
                        !search || target.match(search)
                    );
                }
            };

            $scope.loadLessons = function(course) {
                if(!course.lessons) {
                    Lesson.query({'course__id': course.id}).$promise
                        .then(function(lessons){
                            course.lessons = lessons;
                        });
                }
            }

            Course.query(function(list){
                $scope.courseList = list;
            });
        }
    ]);
})(window.angular);
