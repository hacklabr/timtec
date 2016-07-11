(function(angular){
    'use strict';
    var app = angular.module('my-courses');

    app.controller('UserCourseListController',
        ['$scope', '$window', '$uibModal', 'CertificationProcess', 'CourseStudentService', 'Class',
        function ($scope, $window, $uibModal, CertificationProcess, CourseStudentService, Class) {
            $scope.course_student_list = CourseStudentService.get();
            $window.csl = $scope.course_student_list;
            $window.$scope = $scope;

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
                    cs.certificate.processes = cs.certificate.processes || [];
                    cs.certificate.processes.push(new_cp);
                });
            }

            $scope.hasOpenProcess = function (cs) {
                var course_students = getResource(cs);
                if (course_students && course_students.certificate)
                    return (course_students.certificate.processes.length > 0);
                else
                    return false;
            }

            // FIXME make all app angular
            var getResource = function (cs) {
                for(var i = 0; i < $scope.course_student_list.length; i++){
                    if($scope.course_student_list[i].id == cs)
                        return $scope.course_student_list[i];
                }
                return undefined;
            }
        }
    ]);

    app.controller('UserCertificatesController',
        ['$scope', '$window', '$uibModal', 'CertificationProcess', 'CourseStudentService', 'Class',
        function ($scope, $window, $uibModal, CertificationProcess, CourseStudentService, Class) {
            $scope.course_student_list = CourseStudentService.get();
            console.log($scope.course_student_list);
            $scope.open_evaluation_modal = function(process) {
                var modalInstance = $uibModal.open({
                       templateUrl: 'evaluation_modal.html',
                       controller: EvaluationModalInstanceCtrl,
                       resolve: {
                           process: function () {
                               return process;
                           }
                       }
                });
                modalInstance.result.then(function (process) {
                    console.log($scope.course_student_list);
                });

            };

            var EvaluationModalInstanceCtrl = function($scope, $uibModalInstance, process) {
                $scope.process = process;
                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };
            };
        }
    ]);

    app.controller('AssistantCourseListController', [
        '$scope', '$window', '$uibModal', 'Lesson', 'CourseProfessor', 'Class',
        function ($scope, $window, $uibModal, Lesson, CourseProfessor, Class) {
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
                var modalInstance = $uibModal.open({
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

            var CreateClassModalInstanceCtrl = function($scope, $uibModalInstance, course_professor) {
                $scope.course = course_professor.course;

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };
            };
        }
    ]);

    app.controller('CoordinatorCourseListController', [
        '$scope', '$window', '$uibModal', 'Lesson', 'CourseProfessor', 'Class',
        function ($scope, $window, $uibModal, Lesson, CourseProfessor, Class) {
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
                var modalInstance = $uibModal.open({
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

            var CreateClassModalInstanceCtrl = function($scope, $uibModalInstance, course_professor) {
                $scope.course = course_professor.course;

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };
            };
        }
    ]);

})(window.angular);