(function(angular){
    'use strict';

    var module = angular.module('certification.controllers', []);

    module.controller('EvaluationCtrl', ['$scope', '$modal', '$window', 'CertificationProcess', 'Evaluation',
        function($scope, $modal, $window, CertificationProcess, Evaluation) {
            $scope.errors = {};
            $scope.evaluations = [];

            var cert = document.getElementById('id_user_can_certificate').checked;
            $scope.switches = {
                'can_certificate' : cert
            };

            var match = document.location.href.match(/class\/(\d+)/);
            $scope.klass_id = match[1];

            $scope.createEvaluation = function (evaluation_id) {
                var modalInstance = $modal.open({
                    templateUrl: 'createEvaluationModal.html',
                    controller: ['$scope', '$modalInstance', 'klass_id', 'evaluation_id', CreateUpdateEvaluationModalCtrl],
                    resolve: {
                        klass_id: function () {
                            return $scope.klass_id;
                        },
                        evaluation_id: function(){
                            return evaluation_id ? evaluation_id : false;
                        }
                    }
                });
                modalInstance.result.then(function (evaluation) {
                    if(evaluation.id) {
                        evaluation.$update({}, function (updated_eval) {
                        });
                    } else {
                        evaluation.$save({}, function(new_eval){
                            $scope.evaluations.push(new_eval);
                        });
                    }

                });
            };

            var CreateUpdateEvaluationModalCtrl = function ($scope, $modalInstance, klass_id, evaluation_id) {
                $scope.evaluation;
                if(evaluation_id){
                    Evaluation.get({'id' : evaluation_id}, function(data){
                        $scope.evaluation = data;
                    });
                } else {
                    $scope.evaluation = new Evaluation();
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
            })

        }
    ]);

})(angular);
