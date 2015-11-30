(function(angular){
    'use strict';

    var module = angular.module('certification.controllers', []);

    module.controller('ClassEvaluationsCtrl', ['$scope', 'Evaluation', 'Class',
        function($scope, Evaluation, Class) {
            // Handle Certification:
            // If class has certification, show the evaluation link
            $scope.errors = {};
            $scope.evaluations = [];
        }
    ]);

    module.controller('CertificateCtrl', ['$scope', 'ClassIdGetter', 'Course', 'CourseCertification', 'CertificateTemplate',
        function($scope, ClassIdGetter, Course, CourseCertification, CertificateTemplate){
            console.log(ClassIdGetter.certificateData());
            CourseCertification.get({'link_hash' : ClassIdGetter.certificateData()}, function(data) {
                $scope.cc = data;

                Course.get({'id' : $scope.cc.course}, function(data) {
                    $scope.course = data;
                    console.log(data);
                });

                CertificateTemplate.get({'course' : $scope.cc.course }, function(data) {
                    $scope.ct = data;
                });
            });
        }
    ]);

    module.controller('CertificateTemplateCtrl', ['$scope', 'FormUpload', 'ClassIdGetter', 'Course', 'CertificateTemplate',
        function($scope, FormUpload, ClassIdGetter, Course, CertificateTemplate){

            $scope.course_id = ClassIdGetter.courseSettings();

            Course.get({'id' : $scope.course_id}, function(data) {
                $scope.course = data;
            });

            CertificateTemplate.get({'course' : $scope.course_id}, function(data) {
                $scope.ct = data;
            }, function(error){
                if(error.status == 404){
                    var ct = new CertificateTemplate();
                    ct.course = $scope.course_id;
                    ct.$save({}, function(template){
                        $scope.ct = template;
                    }, function(error){
                        console.log(error);
                    });
                }
            });

            $scope.saveTemplate = function () {
                $scope.ct.$update({'course' : $scope.course_id}, function(updated){
                    $scope.alert.success('Template atualizado.');
                })
            }

            $scope.images = {};

            $scope.saveLogo = function() {
                if(!$scope.images.logo) return;
                if ($scope.course_id) saveImageData();
            };

            $scope.saveSignature = function() {
                if(!$scope.images.signature) return;
                if ($scope.course_id) saveImageData();
            };

            var saveImageData = function(){
                var fu = new FormUpload();
                if($scope.images.logo){
                    fu.addField('logo', $scope.images.logo);
                }
                if($scope.images.signature){
                    fu.addField('signature', $scope.images.signature);
                }
                fu.addField('course', $scope.course_id);
                // return a new promise that file will be uploaded

                return fu.sendTo('/api/certificate_template_images/' + $scope.course_id)
                    .then(function(){
                        $scope.alert.success('A imagem foi atualizada.');
                    });
            }

        }
    ]);

    module.controller('EvaluationCtrl', ['$scope', '$modal', '$window', 'CertificationProcess', 'Evaluation', 'Class', 'ClassIdGetter',
        function($scope, $modal, $window, CertificationProcess, Evaluation, Class, ClassIdGetter) {
            $scope.errors = {};
            $scope.evaluations = [];

            $scope.stats = {
                has_certificate : 0,
                user_can_certificate : 0,
                user_can_attend : 0,
                upcoming : 0
            };

            $scope.switches = {
                can_certificate : false,
            }

            $scope.klass_id = ClassIdGetter.classEditView();

            Class.get({'id' : $scope.klass_id}, function(klass){
                $scope.klass = klass;
                $scope.class_students = klass.students;
                $scope.switches.can_certificate = klass.user_can_certificate;
            });

            Evaluation.query({'klass' : $scope.klass_id}, function(data){
                $scope.class_evaluations = data;

                if($scope.class_evaluations.length > 0) {
                    var now = new Date().getTime();
                    var next_week = now + 7*24*60*60;

                    for(var i = 0; i < $scope.class_evaluations.length; i++) {
                        evaluation = $scope.class_evaluations[i];
                        var e_date = new Date(evaluation.date).getTime();
                        if ((e_date > now) && (e_date <= next_week)) {
                            $scope.stats.upcoming++;
                        }
                    }
                    $scope.evaluation = $scope.class_evaluations[0];
                    window.evaluations = data;
                }
            });


            CertificationProcess.query({'klass' : $scope.klass_id}, function(data){
                $scope.certification_processes = data;
                for(var i = 0; i < $scope.certification_processes.length; i++){
                    var proc = $scope.certification_processes[i];
                    if(proc.course_certification){
                        $scope.stats.user_can_certificate++;
                        if(!proc.evaluation){
                            $scope.stats.user_can_attend++;
                        }
                    }
                    if(proc.approved){
                        $scope.stats.has_certificate++;
                    }
                }
            });

            $scope.toggleClassCertifiable = function (){
                $scope.switches.can_certificate = false;
                $scope.klass.$update(function(klass){
                    $scope.switches.can_certificate = klass.user_can_certificate;
                })
            }

            $scope.addStudentEvaluation = function () {
                var modalInstance = $modal.open(
                    {
                        animation: true,
                        templateUrl: 'addStudentModal.html',
                        controller: ['$scope', '$modalInstance', 'processes', 'evaluation', AddStudentModalCtrl],
                        resolve: {
                            processes: function () {
                                return $scope.certification_processes;
                            },
                            evaluation: function() {
                                return $scope.evaluation;
                            }
                        }
                    }
                );

                modalInstance.result.then(function (class_students) {
                    $scope.user_can_attend = class_students;

                    for(var i = 0; i < $scope.user_can_attend.length; i++){
                        var proc = $scope.user_can_attend[i];

                        if(proc.selected){
                            proc.evaluation = $scope.evaluation.id;
                            proc.$update({}, function(process){

                            });
                        }
                    }
                });
            };

            var AddStudentModalCtrl = function ($scope, $modalInstance, processes, evaluation) {
                $scope.class_students = processes;

                $scope.evaluation = evaluation;

                $scope.selectAll = function (select){
                    for(var i = 0; i < $scope.class_students.length; i++){
                        $scope.class_students[i].selected = select;
                    }
                }

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };

                $scope.save = function(){
                    $modalInstance.close($scope.class_students);
                }
            }

            $scope.createEvaluation = function (isEdit) {
                var modalInstance = $modal.open(
                    {
                        animation: true,
                        templateUrl: 'createEvaluationModal.html',
                        controller: ['$scope', '$modalInstance', 'klass_id', 'evaluation', CreateUpdateEvaluationModalCtrl],
                        resolve: {
                            klass_id: function () {
                                return $scope.klass_id;
                            },
                            evaluation: function() {
                                if(isEdit){
                                    return $scope.evaluation;
                                } else {
                                    return undefined;
                                }
                            }
                        }
                    }
                );

                modalInstance.result.then(function (evaluation) {
                    if(evaluation.id){
                        evaluation.$update({}, function(updated_eval){
                            // console.log(updated_eval);
                        });
                    } else {
                        evaluation.$save({}, function (new_eval) {
                            $scope.class_evaluations.push(new_eval);
                        });
                    }
                });
            };

            $scope.changeEvaluation = function ($event, $index) {
                $event.preventDefault();
                $scope.evaluation = $scope.class_evaluations[$index];
            };

            var CreateUpdateEvaluationModalCtrl = function ($scope, $modalInstance, klass_id, evaluation) {
                if(!evaluation){
                    $scope.evaluation = new Evaluation();
                } else {
                    $scope.evaluation = evaluation;
                }

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };

                $scope.openCalendar = function(e, b){
                    e.preventDefault();
                    e.stopPropagation();
                    $scope.calendar[b] = true;
                }

                $scope.calendar = {
                    'eval_date' : false,
                    'eval_results_date' : false
                }

                $scope.save = function(){
                    // Write validation
                    $scope.evaluation.klass = klass_id;
                    $modalInstance.close($scope.evaluation);
                }
            }


            $scope.isCurrent = function(evaluation_id){
                return evaluation_id == $scope.evaluation.id;
            }

            var evaluation = function($index){
                return $index >= 0 ? $scope.class_evaluations[$index] : false;
            }

            var class_students = function(){
                return $scope.class_students;
            }

        }
    ]);

})(angular);
