(function(angular){
    'use strict';

    var module = angular.module('edit_class.controllers', []);

    // Service to share data across the controllers
    module.factory('classe_list', function() {
        return {
            classe : []
        };
    });

    module.controller('ClassesListController', ['$scope', '$location', 'Class', 'Contracts', 'Course',
        function($scope, $location, Class, Contracts, Course) {
            var url_path = $location.absUrl().split('/');
            var course_slug = url_path.slice(-3)[0];

            $scope.classes = {};

            var course;
            Course.query({slug: course_slug}).$promise.then(function(response) {
                course = response[0];
                $scope.classes.all = Class.query({course: course.id});
                $scope.classes.filtered = $scope.classes.all;
            });

            $scope.contracts = Contracts.query({'simple' : true});
            $scope.filters = {
                contract: ''
            };

            $scope.$watch('filters.contract', function(newContract, oldContract) {
                if (!newContract)
                    $scope.classes.filtered = $scope.classes.all;
                else if (newContract)
                    $scope.classes.filtered = $scope.classes.all.filter(function(klass) {
                        if (klass.contract)
                            return klass.contract.id === newContract.id;
                        return false;
                    });
            });
        }
    ]);

    module.controller('EditClassController', ['$scope', '$window', '$filter', 'Class', 'StudentSearch', 'Contracts', 'CourseCertification',
        function($scope, $window, $filter, Class, StudentSearch, Contracts, CourseCertification) {

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

            $scope.contracts = Contracts.query({'simple' : true});

            $scope.getUsers = function(val) {
                return new StudentSearch(val, course_id);
            };

            $scope.remove_item = function(index){
                // removing from 'screen' list
                var student_id = $scope.classe.students_details[index].user.id;
                $scope.classe.students_details.splice(index, 1);

                // remove from real list
                var index_management = $scope.classe.students.indexOf(student_id);
                $scope.classe.students.splice(index_management, 1);
                $scope.save();
            };

            $scope.on_select_student = function(model) {
                $scope.classe.students_details.unshift(model);
                $scope.classe.students.unshift(model.id);
                $scope.asyncSelected = '';
                $scope.save();
            };

            $scope.toggle_class_certificable = function (){
                $scope.save();
            }

            $scope.toggle_certificate = function (index){

                var student = $scope.classe.students_details[index];
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
                $scope.save();
            }

            $scope.save = function(){

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
