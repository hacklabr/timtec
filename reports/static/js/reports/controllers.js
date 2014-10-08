
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('ReportsCtrl', ['$scope', '$location', '$sce', '$window', 'CourseUserReport', 'LessonsUserProgress', 'StudentSearch', 'Class', 'CourseStats', 'CourseProfessor',
            function ($scope, $location, $sce, $window, CourseUserReport, LessonsUserProgress, StudentSearch, Class, CourseStats, CourseProfessor) {
                $scope.courseId = /course\/([^\/]+)\/stats/.extract(location.pathname, 1);
                var current_user_id = parseInt($window.user_id, 10);

                $scope.course_stats = CourseStats.get({courseId: $scope.courseId});
                $scope.users_reports = CourseUserReport.query({course: $scope.courseId});

                $scope.my_classes = [];
                $scope.others_classes = [];
                $scope.filters = {};

                CourseProfessor.query({course: $scope.courseId, user: current_user_id}, function(course_professor){
                    var current_user = course_professor[0];
                    $scope.classes = Class.query({course: $scope.courseId}, function(classes){
                        if (current_user.role == 'assistant') {
                            $scope.my_classes = classes;
                            $scope.filters.selected_class = 'my_classes';
                        } else if (current_user.role == 'coordinator') {
                            $scope.filters.selected_class = 'all';
                            classes.forEach(function(klass) {
                                if (klass.assistant == current_user.user) {
                                    $scope.my_classes.unshift(klass);
                                } else {
                                    $scope.others_classes.unshift(klass);
                                }
                            });
                        }
                    });
                    $scope.current_user =  current_user;
                });

                $scope.show_user_progress_details = function(user) {
                    if (user.lessons_stats === undefined) {
                        user.lessons_stats = LessonsUserProgress.get({courseId: $scope.courseId, user: user.user_id});
                    }
                };

                $scope.filter_stats = function(){
                    if ($scope.filters.selected_class == 'all') {
                        $scope.course_stats = CourseStats.get({courseId: $scope.courseId}, function (course_stats){});
                        $scope.users_reports = CourseUserReport.query({course: $scope.courseId}, function (users_reports){});
                    } else if ($scope.filters.selected_class == 'my_classes') {
                        $scope.users_reports = CourseUserReport.query({course: $scope.courseId, classes: $scope.my_classes.map(function(x) {return x.id; })});
                        $scope.course_stats = CourseStats.get({courseId: $scope.courseId, classes: $scope.my_classes.map(function(x) {return x.id; })});
                    } else if ($scope.filters.selected_class == 'others_classes') {
                        $scope.users_reports = CourseUserReport.query({course: $scope.courseId, classes: $scope.others_classes.map(function(x) {return x.id; })});
                        $scope.course_stats = CourseStats.get({courseId: $scope.courseId, classes: $scope.others_classes.map(function(x) {return x.id; })});
                    } else {
                        $scope.users_reports = CourseUserReport.query({course: $scope.courseId, classes: $scope.filters.selected_class});
                        $scope.course_stats = CourseStats.get({courseId: $scope.courseId, classes: $scope.filters.selected_class});
                    }
                };
        }]);
})(angular);
