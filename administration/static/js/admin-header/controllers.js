(function(angular){

    angular.module('adminHeader.controllers', []).
        controller('HeaderController', ['$scope', 'Course',  'CourseProfessor', 'Lesson', '$filter',
        function($scope, Course,  CourseProfessor, Lesson, $filter) {

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
                        // course_material and forum urls
                        $scope.course_url = 'admin/courses/' + course.id;
                        $scope.course_material_url = 'admin/course/' + course.id  + '/material/';
                        $scope.forum_url = 'admin/course/' + course.id +  '/forum/';
                        $scope.messages_url = 'admin/course/' + course.id   + '/messages/';
                        $scope.reports_url = 'admin/course/' + course.id   + '/stats/';
                        $scope.classes_url = 'course/' + course.slug + '/classes/';
                        $scope.permissions_url = 'admin/course/' + course.id + '/permissions/';
                    })
                    .then(function(){
                        $scope.courseProfessors = CourseProfessor.query({ course: match[1], role: 'instructor'});
                        return $scope.courseProfessors.promise;
                    })['catch'](function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    })['finally'](function(){
                        $scope.statusList = Course.fields.status.choices;
                    });
            }
        }
    ]);

})(angular);
