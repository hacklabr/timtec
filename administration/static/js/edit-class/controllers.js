(function(angular){
    'use strict';

    var module = angular.module('edit_class.controllers', []);

    // Service to share data across the controllers
    module.factory('classe_list', function() {
        return {
            classe : []
        };
    });

    module.controller('ClassController', ['$scope', '$window', 'Class', 'StudentSearch',
        function($scope, $window, Class, StudentSearch) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Esta classe não existe!',
                '405': 'Alguma coisa parece ter dado errado!',
            };

            $scope.class_id = parseInt($window.class_id, 10);
            $scope.course_id = parseInt($window.course_id, 10);
            $scope.classe = Class.get({id: $scope.class_id}, function(classe) {

                // if($scope.classe.assistant) {
                //     angular.forEach($scope.classe.course.professors, function(value, key) {
                //         if(value.id == $scope.classe.assistant) {
                //             $scope.classe.assistant = value;
                //         }
                //     });
                // }

                console.log(classe);
                document.title = 'Turma: {0}'.format(classe.name);
            });

            $scope.getUsers = function(val) {
                return new StudentSearch(val, course_id);
            };
            
            $scope.remove_item = function(index){
                $scope.classe.students.splice(index, 1);
                $scope.classe.students_management.splice(index, 1);
                $scope.save();
            };

            $scope.on_select_student = function(model) {
                $scope.classe.students.unshift(model);
                $scope.classe.students_management.unshift(model.id);
                $scope.asyncSelected = '';
                $scope.save();
            };
            
            $scope.save = function(){

                if($scope.classe.assistant) {
                    $scope.classe.assistant_management = $scope.classe.assistant.id;
                }
                
                $scope.classe.$update()
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso.');
                        
                        // remove pop-up that confirm if user go without save changes
                        window.onbeforeunload = function(){};

                        })['catch'](function(resp){
                            $scope.alert.error(httpErrors[resp.status.toString()]);
                        });
            }


        }
    ]);
})(angular);
