(function(angular){
    'use strict';

    var module = angular.module('edit_class.controllers', []);

    // Service to share data across the controllers
    module.factory('classe_list', function() {
        return {
            classe : []
        };
    });

    module.controller('ClassController', ['$scope', '$window', 'Class', 'StudentSearch', 'CourseCertification',
        function($scope, $window, Class, StudentSearch, CourseCertification) {

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
                document.title = 'Turma: {0}'.format(classe.name);
            });

            $scope.getUsers = function(val) {
                return new StudentSearch(val, course_id);
            };

            $scope.remove_item = function(index){
                // removing from 'screen' list
                var student_id = $scope.classe.students[index].user.id;
                $scope.classe.students.splice(index, 1);

                // remove from real list
                var index_management = $scope.classe.students_management.indexOf(student_id);
                $scope.classe.students_management.splice(index_management, 1);
            };

            $scope.on_select_student = function(model) {
                $scope.classe.students.unshift(model);
                $scope.classe.students_management.unshift(model.id);
                $scope.asyncSelected = '';
                $scope.save();
            };

            $scope.toggle_certificate = function (index){

                var student = $scope.classe.students[index];
                if(student.certificate) {
                    var cc_id = student.certificate.link_hash;
                    var user_id = student.user.id;
                    var cc = CourseCertification.get({link_hash: cc_id, user: user_id}, function(classe) {
                        if(cc.type == 'receipt') {
                            cc.type = 'certificate';
                        } else {
                            cc.type = 'receipt';
                        }
                        cc.$update({link_hash: cc_id, user: user_id});
                    });
                }
            }

            $scope.save = function(){

                $scope.classe.$resolved = false;
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
            };

        }
    ]);
})(angular);
