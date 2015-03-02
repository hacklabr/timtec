(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.controller('CoursesAdminController', [
        '$scope', '$modal', 'Course', 'Lesson',
        function ($scope, $modal, Course, Lesson) {

            $scope.courseList = [];
            $scope.ordering = 'start_date';
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
            };

            Course.query(function(list){
                $scope.courseList = list;
            });

            $scope.import_course_modal = function () {
                var modalInstance = $modal.open({
                    templateUrl: 'import_course_modal.html',
                    controller: ['$scope', '$modalInstance', ImportCourseModalInstanceCtrl],
                    //resolve: {
                    //    course_id: function () {
                    //        return $scope.course_id;
                    //    }
                    //}
                });
                modalInstance.result.then(function (new_message) {
                    //new_message.$save({}, function(new_message){
                    //    messages_list.messages.unshift(new_message);
                    //    $rootScope.$broadcast('newMessage');
                    //});

                });
            };
            var ImportCourseModalInstanceCtrl = function ($scope, $modalInstance) {
                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };
            };
        }
    ]);


    app.controller('CourseListByUserRoleController', [
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
