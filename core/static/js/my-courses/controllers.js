(function(angular){
    'use strict';
    var app = angular.module('my-courses');

    app.controller('UserCourseListController',
        ['$scope', '$window', '$modal', 'CertificationProcess', 'CourseStudentService', 'Class', 'CompletedCoursesService',
        function ($scope, $window, $modal, CertificationProcess, CourseStudentService, Class, CompletedCoursesService) {
            $scope.course_students = CourseStudentService.get();

            // FIXME delete two line above
//            $window.csl = $scope.course_students;
//            $window.$scope = $scope;

//            $scope.courses_cert_process = CompletedCoursesService.courses_cert_process

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
                    CompletedCoursesService.courses_cert_process.push(new_cp)
                });
            }

            $scope.hasOpenProcess = function (cs) {
                CompletedCoursesService.courses_cert_process.forEach(function(course_certificate){
                    if (course_certificate.course_student == cs)
                        return true;
                })
                return false;
//                cs = getResource(cs);
//                for(var i = 0; i < CompletedCoursesService.courses_cert_process; i++){
//                    if(cs.certificate.processes[i].approved) return false;
//                }
//                return true;
//                if (cs === undefined)
//                    return false;
//                else
//                    return true;
            }

            // FIXME make all app angular
            var getResource = function (cs) {
                for(var i = 0; i < $scope.course_students.length; i++){
                    if($scope.course_students[i].id == cs)
                        return $scope.course_students[i];
                }
                return undefined;
            }
        }
    ]);

    app.controller('UserCertificatesController',
        ['$scope', '$modal', 'CurrentUser', 'CertificationProcess', 'CourseCertification', 'CompletedCoursesService',
        function ($scope, $modal, CurrentUser, CertificationProcess, CourseCertification, CompletedCoursesService) {

            CompletedCoursesService.completed_courses = CourseCertification.query({user: CurrentUser.id}, function(courses_certifications) {
                courses_certifications.forEach(function(course_certification) {
                    if (course_certification.processes.length > 0) {
                        CompletedCoursesService.courses_cert_process.unshift(course_certification);
                    } else if (course_certification.type === 'certificate' && course_certification.is_valid) {
                        CompletedCoursesService.courses_certificates.unshift(course_certification);
                    } else if (course_certification.type === 'receipt' && course_certification.is_valid) {
                        CompletedCoursesService.courses_receipts.unshift(course_certification);
                    }
                })
            })

            $scope.courses_receipts = CompletedCoursesService.courses_receipts;
            $scope.courses_certificates = CompletedCoursesService.courses_certificates;
            $scope.courses_cert_process = CompletedCoursesService.courses_cert_process;

            $scope.open_evaluation_modal = function(process) {
                var modalInstance = $modal.open({
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

            var EvaluationModalInstanceCtrl = function($scope, $modalInstance, process) {
                $scope.process = process;
                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };
            };
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