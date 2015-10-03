(function(angular){
    'use strict';

    var module = angular.module('certification.controllers', []);

    module.service('ClassIdGetter', ['$window', function($window){
        return {
            'classEditView' : function(){
                var match = document.location.href.match(/class\/(\d+)/);
                return match[1];
            },

        }
    }]);

    module.filter('attending', function() {
        return function (items, evaluation_id){
            if(!items || !evaluation_id) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                console.log(items[i].klass);
                if (evaluation_id == items[i].evaluation) filtered.push(items[i]);
            }
            return filtered;
        }
    });

    module.controller('ClassEvaluationsCtrl', ['$scope', '$modal', '$window', 'CertificationProcess', 'Evaluation', 'Class',
        function($scope, Evaluation, Class) {
            // Handle Certification:
            // If class has certification, show the evaluation link
            $scope.errors = {};
            $scope.evaluations = [];

            var cert = document.getElementById('id_user_can_certificate').checked;
            $scope.switches = {
                'can_certificate' : cert
            };

        }
    ]);

    module.controller('EvaluationCtrl', ['$scope', '$modal', '$window', 'CertificationProcess', 'Evaluation', 'Class', 'ClassIdGetter',
        function($scope, $modal, $window, CertificationProcess, Evaluation, Class, ClassIdGetter) {
            $scope.errors = {};
            $scope.evaluations = [];


            $scope.klass_id = ClassIdGetter.classEditView();

            $scope.class_students = Class.get({'id' : $scope.klass_id}, function(klass){
                $scope.klass = klass;
                $scope.class_students = klass.students;
            });

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
                            // $scope.class_evaluations.push(updated_eval);
                            console.log(updated_eval);
                        });
                    } else {
                        evaluation.$save({}, function (new_eval) {
                            $scope.class_evaluations.push(new_eval);
                        });
                    }
                });
            };

            $scope.changeEvaluation = function ($index) {
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

            Evaluation.query({'klass' : $scope.klass_id}, function(data){
                $scope.class_evaluations = data;
                if($scope.class_evaluations.length > 0) {
                    $scope.evaluation = $scope.class_evaluations[0];
                }
            });

            CertificationProcess.query({'klass' : $scope.klass_id}, function(data){
                $scope.certification_processes = data;
            });

            $scope.selectAll = function (select){
                // if(select){
                for(var i = 0; i < $scope.class_students.length; i++){
                    $scope.class_students[i].selected = select;
                }
                //}
            }

            $scope.selectItem = function($event, item){
                console.log($event);
                console.log(item);
            }


            $scope.selected_students = [];
            var showSelected = function(){
                for(var i = 0; i > $scope.class_students; i++){
                    $scope.selected_students[i] = false;
                }
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
