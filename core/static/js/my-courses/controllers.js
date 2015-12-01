(function(angular){
    'use strict';
    var app = angular.module('my-courses');

    app.controller('UserCourseListController', ['$scope', '$window', '$modal', 'Lesson', 'CourseProfessor', 'Class',
        function ($scope, $window, $modal, Lesson, CourseProfessor, Class) {
            $scope.createCertificationProcess = function(cs){
                console.log(cs);
                // TODO: create certification process and change tab
                /*
                    Create a new certification process with or without
                    a course certification (in this case, type receipt)

                    We are going to use user and course certification

                    After creation, We change the tab to the my certificates
                    tab. In this tab, the use can see all data about certification
                    such as evaluation date, grade and future approval (or not)

                */
            }
        }
    ]);

    app.controller('AssistantCourseListController', [
        '$scope', '$window', '$modal', 'Lesson', 'CourseProfessor', 'Class',
        function ($scope, $window, $modal, Lesson, CourseProfessor, Class) {
            var current_user_id = parseInt($window.user_id, 10);

            $scope.loadLessons = function(course) {
                if(!course.lessons) {
                    Lesson.query({'course__id': course.id}).$promise
                        .then(function(lessons){
                            course.lessons = lessons;
                        });
                }
            };

            $scope.courses_user_assist = CourseProfessor.query({'user': current_user_id,
                          'role': 'assistant'});

            $scope.courses_user_coordinate = CourseProfessor.query({'user': current_user_id,
                          'role': 'coordinator'});

            $scope.open_professor_modal = function(course_professor) {
                var modalInstance = $modal.open({
                       templateUrl: 'create_class_modal.html',
                       controller: CreateClassModalInstanceCtrl,
                       resolve: {
                           course_professor: function () {
                               return course_professor;
                           }
                       }
                });
                modalInstance.result.then(function (course_professor) {
                });
            };

            var CreateClassModalInstanceCtrl = function($scope, $modalInstance, course_professor) {
                $scope.course = course_professor.course;

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };
            };
        }
    ]);

    app.controller('CoordinatorCourseListController', [
        '$scope', '$window', '$modal', 'Lesson', 'CourseProfessor', 'Class',
        function ($scope, $window, $modal, Lesson, CourseProfessor, Class) {
            var current_user_id = parseInt($window.user_id, 10);

            $scope.loadLessons = function(course) {
                if(!course.lessons) {
                    Lesson.query({'course__id': course.id}).$promise
                        .then(function(lessons){
                            course.lessons = lessons;
                        });
                }
            };

            $scope.courses_user_assist = CourseProfessor.query({'user': current_user_id,
                          'role': 'assistant'});

            $scope.courses_user_coordinate = CourseProfessor.query({'user': current_user_id,
                          'role': 'coordinator'});

            $scope.open_professor_modal = function(course_professor) {
                var modalInstance = $modal.open({
                       templateUrl: 'create_class_modal.html',
                       controller: CreateClassModalInstanceCtrl,
                       resolve: {
                           course_professor: function () {
                               return course_professor;
                           }
                       }
                });
                modalInstance.result.then(function (course_professor) {
                });
            };

            var CreateClassModalInstanceCtrl = function($scope, $modalInstance, course_professor) {
                $scope.course = course_professor.course;

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };
            };
        }
    ]);

})(window.angular);