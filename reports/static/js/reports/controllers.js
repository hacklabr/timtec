
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('reports.controllers', []).
        controller('ReportsCtrl', ['$scope', '$location', '$sce', '$window', 'CourseUserReport', 'LessonsUserProgress', 'Class', 'CourseStats', 'CourseProfessor',
            function ($scope, $location, $sce, $window, CourseUserReport, LessonsUserProgress, Class, CourseStats, CourseProfessor) {
                $scope.course_id = parseInt($window.course_id, 10);
                $scope.user_id = parseInt($window.user_id, 10);
                $scope.current_user_role = null;

                $scope.currentPage = 1;
                $scope.query = {
                        page: $scope.currentPage,
                        course: $scope.course_id,
                        ordering: $scope.sort,
                        s: "",
                        selected_class: "",
                    }

                var get_items = function() {
                    $scope.query.page = $scope.currentPage;
                    $scope.course_stats = CourseStats.get({courseId: $scope.course_id});
                    $scope.users_reports = CourseUserReport.query($scope.query, function (data) {
                        $scope.totalItems = data.count;
                    });
                }

                get_items();
                $scope.$watch('currentPage', function(){
                    get_items();
                });

                $scope.$watch('query', function(){
                    $scope.filter_stats();
                });

                $scope.filter_stats = function() {
                    $scope.currentPage = 1;
                    $scope.query.page = $scope.currentPage;
                    get_items();
                }

                $scope.filter_invert = function() {
                    $scope.query.reverse = !$scope.query.reverse;
                    $scope.filter_stats();
                }

                CourseProfessor.query({course: $scope.course_id, user: $scope.user_id}, function(course_professor){
                    var current_user = course_professor[0];
                    var current_user_role = '';
                    // If current_user is undefined, he is not course professor, but may be admin
                    if (current_user === undefined) {
                        if ($window.is_admin)
                            // if user is admin, set role to coordinator, higher role in course.
                            current_user_role = 'coordinator';
                    } else {
                        current_user_role = current_user.role;
                    }

                    $scope.classes = Class.query({course: $scope.course_id}, function(classes){
                        if (current_user_role == 'assistant') {
                            $scope.my_classes = classes;
                            $scope.query.selected_class = 'my_classes';
                        } else if (current_user_role == 'coordinator') {
                            $scope.query.selected_class = 'all';
                        }
                    });
                    $scope.current_user_role =  current_user_role;
                });

                $scope.show_user_progress_details = function(user) {
                    if (user.lessons_stats === undefined) {
                        user.lessons_stats = LessonsUserProgress.get({courseId: $scope.course_id, user: user.user_id});
                    }
                };

        }]);
})(angular);
