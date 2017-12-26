(function(angular){
    'use strict';

    var module = angular.module('certification');

    module.controller('CourseClassesController', ['$scope', '$window', 'Evaluation', 'CourseClassesService',
        function($scope, $window, Evaluation, CourseClassesService) {
            // Handle Certification:
            // If class has certification, show the evaluation link
            $scope.errors = {};
            $scope.course_klasses = CourseClassesService.getClasses();
            console.log($scope.course_klasses);
        }
    ]);

    module.controller('CertificateCtrl', ['$scope', 'ClassIdGetter', 'Course', 'CourseCertification', 'CertificateTemplate',
        function($scope, ClassIdGetter, Course, CourseCertification, CertificateTemplate){
            console.log(ClassIdGetter.certificateData());
            $scope.certificate = CourseCertification.get({'link_hash' : ClassIdGetter.certificateData()}, function(certificate) {
//                $scope.certificate = data;

                $scope.course = Course.get({'id' : certificate.course});

                $scope.cert_template = CertificateTemplate.get({'course' : certificate.course });
                return certificate;
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
                    var success = true;
                    var pr = saveImageData();
                    pr.then(function(data){

                    }, function(error){
                        var msg = error.data.signature.length ?
                                error.data.signature[0] :
                                "Erro no envio da imagem";
                        $scope.alert.error(msg);
                        success = false;
                    });
                    if (success) {
                        $scope.alert.success('Opções salvas com sucesso!');
                    }
                })
            }

            $scope.images = {};

            var saveImageData = function(){
                var fu = new FormUpload();
                if($scope.images.cert_logo){
                    fu.addField('cert_logo', $scope.images.cert_logo);
                }
                if($scope.images.base_logo){
                    fu.addField('base_logo', $scope.images.base_logo);
                }
                if($scope.images.site_logo){
                    fu.addField('site_logo', $scope.images.site_logo);
                }
                if($scope.images.signature){
                    fu.addField('signature', $scope.images.signature);
                }

                return fu.sendTo('/paralapraca/api/certificate_template_images/' + $scope.certificate_id);
            }

        }
    ]);

    module.controller('CertificateDataAdminController', [
        '$scope', '$uibModal', '$window', 'CertificateData', 'Course',
        function ($scope, $uibModal, $window, CertificateData, Course) {
            $scope.certificateList = [];
            $scope.ordering = 'certificate_template.course';
            $scope.reverse = false;
            $scope.filters = {
                type: 'all',
                course: false,
                contract : false,
                textsearch: '',
                check : function(c_data){
                    var f = $scope.filters;
                    var search = f.textsearch.toLowerCase();
                    var target = c_data.certificate_template.course_name.toLowerCase();
                    f.is_clear = f.type == 'all' && !f.course && !f.contract && f.textsearch == ''
                    return (
                        f.type == 'all' || c_data.type == f.type
                    ) && (
                        !search || target.match(search)
                    ) && (
                        !f.contract || c_data.contract.id == f.contract
                    ) && (
                        !f.course || c_data.certificate_template.course == f.course
                    );
                },
                is_clear: true,
                clear: function(){
                    var f = $scope.filters;
                    f.type = 'all';
                    f.course = f.contract = false;
                    f.textsearch = '';
                    f.is_clear = true;
                }
            };

            $scope.generate_templates_modal = function () {
                var modalInstance = $uibModal.open({
                    templateUrl: 'generate_templates_modal.html',
                    controller: ['$scope', '$uibModalInstance', 'CertificateData', 'Contract', 'certificateFormList', 'courses', CertificateModalInstanceCtrl],
                    resolve: {
                        certificateFormList: () => { return $scope.certificateList; },
                        courses: () => { return $scope.courses; }
                    }
                });
                modalInstance.result.then(function (response) {
                    loadData();
                });
            };

            var CertificateModalInstanceCtrl = function ($scope, $uibModalInstance, CertificateData, Contract, certificateFormList, courses) {
                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };

                $scope.certificateFormList = certificateFormList;
                Contract.query({}, function(data){
                    $scope.contracts = data;
                });
                $scope.courses = courses;

                $scope.form_filters = {
                    type: 'all',
                    course: false,
                    contract : false,
                    check : function(c_data){
                        var f = $scope.form_filters;
                        var target = c_data.certificate_template.course_name.toLowerCase();
                        f.has_data = f.course && f.contract
                        if (!f.has_data){
                            return false;
                        }
                        return (
                            f.type == 'all' || c_data.type == f.type
                        ) && (
                            !f.contract || c_data.contract.id == f.contract
                        ) && (
                            !f.course || c_data.certificate_template.course == f.course
                        );
                    },
                    has_data: false,
                };

                $scope.generate_templates = function () {
                    var c_data = new CertificateData({
                        contract: $scope.form_filters.contract,
                        course: $scope.form_filters.course,
                        generate: true
                    });
                    c_data.$save((data) => {
                        $uibModalInstance.close(data);
                    }, (error) => {
                        $uibModalInstance.close(error);
                    });
                };
            };

            var loadData = () => {
                CertificateData.query({}, function(list){
                    $scope.certificateList = list;
                    $scope.certificateFormList = list;
                    var contracts = list.map(function(item){
                        return item.contract;
                    }).reduce(function(prev, curr, i, arr){
                        var index = prev.findIndex(function(item){
                            return item.id == curr.id
                        });
                        index < 0 ? prev.push(curr) : prev;
                        return prev;
                    }, []);

                    $scope.contracts = contracts;
                });
            }
            loadData();

            Course.query({}, function(courses) {
                $scope.courses = courses;
            })

        }
    ]);

    module.controller('ClassEvaluationsController',
    ['$scope', '$uibModal', '$window', '$routeParams', 'CertificationProcess', 'Evaluation', 'Class', 'ClassIdGetter',
    function($scope, $uibModal, $window, $routeParams, CertificationProcess, Evaluation, Class, ClassIdGetter) {
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

            // FIXME this controller is being used in more than one view with different parameters
            if($routeParams['klassId']) {
                $scope.klass_id = $routeParams['klassId'];
            } else {
                $scope.klass_id = ClassIdGetter.classEditView();
            }

            Class.get({'id' : $scope.klass_id}, function(klass){
                $scope.klass = klass;
                $scope.class_students = klass.students;
                $scope.switches.can_certificate = klass.user_can_certificate;
                $scope.class_evaluations = klass.evaluations;

                if($scope.class_evaluations.length > 0) {
                    var now = new Date().getTime();
                    var next_week = now + 7*24*60*60*1000;

                    for(var i = 0; i < $scope.class_evaluations.length; i++) {
                        evaluation = $scope.class_evaluations[i];
                        var e_date = new Date(evaluation.date).getTime();
                        if ((e_date > now) && (e_date <= next_week)) {
                            $scope.stats.upcoming++;
                        }
                    }
                    $scope.evaluation = $scope.class_evaluations[0];
                }

                $scope.certification_processes = klass.processes;
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
                var modalInstance = $uibModal.open(
                    {
                        animation: true,
                        templateUrl: 'addStudentModal.html',
                        controller: ['$scope', '$uibModalInstance', 'processes', 'evaluation', 'students', AddStudentModalCtrl],
                        resolve: {
                            processes: function () {
                                return $scope.certification_processes;
                            },
                            evaluation: function() {
                                return $scope.evaluation;
                            },
                            students: function() {
                                return $scope.class_students;
                            }
                        }
                    }
                );

                modalInstance.result.then(function (class_students) {
                    $scope.user_can_attend = class_students;

                    for(var i = 0; i < $scope.user_can_attend.length; i++){
                        var proc = $scope.user_can_attend[i];
                        if(proc.selected){
                            proc.selected = false;
                            proc.evaluation = $scope.evaluation.id;
                            if(proc.student.id){
                                proc.student = proc.student.id;
                            }
                            proc = new CertificationProcess(proc);

                            proc.$update({}, function(process, data){
                                $scope.evaluation.processes.push(process.id);
                                $scope.certification_processes.filter(function(s){return s.id == process.id;})[0] = process;
                                $scope.stats.user_can_attend--;
                            });
                        }
                    }
                });

            };

            var AddStudentModalCtrl = function ($scope, $uibModalInstance, processes, evaluation, students) {
                $scope.certification_processes = processes;
                $scope.class_students = students;
                $scope.evaluation = evaluation;

                $scope.selectAll = function (select){
                    for(var i = 0; i < $scope.certification_processes.length; i++){
                        if(!$scope.certification_processes[i].evaluation
                                && $scope.certification_processes[i].course_certification)
                            $scope.certification_processes[i].selected = select;
                    }
                }

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };

                $scope.save = function(){
                    $uibModalInstance.close($scope.certification_processes);
                }
            }

            $scope.createEvaluation = function (isEdit) {
                var modalInstance = $uibModal.open(
                    {
                        animation: true,
                        templateUrl: 'createEvaluationModal.html',
                        controller: ['$scope', '$uibModalInstance', 'klass_id', 'evaluation', CreateUpdateEvaluationModalCtrl],
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

            var CreateUpdateEvaluationModalCtrl = function ($scope, $uibModalInstance, klass_id, evaluation) {
                if(!evaluation){
                    $scope.evaluation = new Evaluation();
                } else {
                    $scope.evaluation = evaluation;
                }

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
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
                    $uibModalInstance.close($scope.evaluation);
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
