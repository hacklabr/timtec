(function(angular){
    'use strict';
    var app = angular.module('my-courses');

    app.controller('UserCourseListController',
        ['$scope', '$window', '$modal', 'CertificationProcess', 'CourseStudent', 'Class',
        function ($scope, $window, $modal, CertificationProcess, CourseStudent, Class) {
            CourseStudent.query(function (cs){
               $scope.course_student_list = cs;
               console.log(cs);
            })


            $scope.createCertificationProcess = function (cs){
                var cp = new CertificationProcess();
                cs = getResource(cs);
                cp.student = cs.user.id;
                cp.klass = cs.current_class.id;
                if(!cs.certificate)
                    cp.course_certification = null;
                else {
                    cp.course_certification = cs.certificate.link_hash;
                }
                cp.evaluation = null;
                cp.$save(function(new_cp){
                    $('#dashboard-tabs a[href=#my-certificates]').tab('show');
                });
            }


            var getResource = function (cs) {
                for(var i = 0; i < $scope.course_student_list.length; i++){
                    if($scope.course_student_list[i].id == cs)
                        return $scope.course_student_list[i];
                }
                return undefined;
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