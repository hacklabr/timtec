(function(angular){

    angular.module('adminHeader.controllers', []).
        controller('HeaderController', ['$scope', 'Course',  'CourseProfessor', 'Lesson', '$filter', 'FormUpload',
        function($scope, Course,  CourseProfessor, Lesson, $filter, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/course\/([0-9]+)/);
            $scope.course = new Course();
            $scope.courseProfessors = [];
            window.s = $scope;
            $scope.templateUrl = '/static/templates/admin_header.html';
            if( match ) {
                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        document.title = 'Curso: {0}'.format(course.name);
                        $scope.addThumb = !course.thumbnail_url;
                        // course_material and forum urls
                        $scope.course_material_url = 'admin/course/' + course.slug  + '/material/';
                        $scope.forum_url = 'admin/course/' + course.id +  '/forum/';
                    })
                    .then(function(){
                        $scope.courseProfessors = CourseProfessor.query({ course: match[1] });
                        return $scope.courseProfessors.promise;
                    })['catch'](function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    })['finally'](function(){
                        $scope.statusList = Course.fields.status.choices;
                    });
            }

            function showFieldErrors(response) {
                $scope.errors = response.data;
                var messages = [];
                for(var att in response.data) {
                    var message = response.data[att];
                    if(Course.fields && Course.fields[att]) {
                        message = Course.fields[att].label + ': ' + message;
                    }
                    messages.push(message);
                }
                $scope.alert.error('Encontramos alguns erros!', messages, true);
            }

            $scope.deleteProfessor = function(courseProfessor) {
                var professor_name = courseProfessor.user_info.name;
                var msg = 'Tem certeza que deseja remover "{0}" da lista de professores deste curso?'.format(professor_name);
                if(!window.confirm(msg)) return;

                courseProfessor.$delete().then(function(){
                    var filter = function(p) { return p.user !== courseProfessor.user; };
                    $scope.courseProfessors = $scope.courseProfessors.filter(filter);
                    $scope.alert.success('"{0}" foi removido da list.'.format(professor_name));
                });
            };

            $scope.saveProfessor = function(courseProfessor) {
                function __saveProfessor(){
                    if (!$scope.course.id) {
                        return $scope.course.save().then(function(course){
                            courseProfessor.course = course.id;
                            return courseProfessor.saveOrUpdate();
                        });
                    }
                    return courseProfessor.saveOrUpdate();
                }
                return __saveProfessor().then(function(){
                    $scope.alert.success('{0} foi atualizado'.format(courseProfessor.user_info.name));
                });
            };

            $scope.addProfessor = function(professor) {
                if(!professor) return;
                var copy = angular.copy(professor);

                var reduce = function(a,b){ return a || b.user === copy.id; };

                if($scope.courseProfessors.reduce(reduce, false)) {
                    $scope.alert.error('"{0}" já está na lista de professores deste curso.'.format(copy.name));
                    return;
                }

                var professorToAdd = new CourseProfessor({
                    'user': copy.id,
                    'course': $scope.course.id,
                    'biography': copy.biography,
                    'role': 'instructor',
                    'user_info': copy
                });

                $scope.saveProfessor(professorToAdd).then(function(){
                    $scope.alert.success('"{0}" foi adicionado a lista de professores.'.format(copy.name));
                    $scope.courseProfessors.push(professorToAdd);
                })['catch'](showFieldErrors);
            };

            $scope.repositionInstructors = function() {
                $scope.courseProfessors.forEach(function(p, i){
                    p.position = i;
                });
            };

            $scope.saveAllInstructors = function() {
                var i = 0;
                function __saveInstructors() {
                    if(i < $scope.courseProfessors.length) {
                        return $scope.courseProfessors[i++]
                                     .saveOrUpdate()
                                     .then(__saveInstructors);
                    }
                }

                $scope.alert.warn('Atualizando dados dos professores');

                __saveInstructors()
                    .then(function(){
                        $scope.alert.success('Os dados dos professores foram atualizados.');
                    })['catch'](function(){
                        $scope.alert.error('Algum problema impediu a atualização dos dados dos professores.');
                    });
            };
        }
    ]);

})(angular);
