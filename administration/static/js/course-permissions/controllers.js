(function(angular){

    angular.module('course-permissions.controllers', []).
        controller('PermissionsController', ['$scope', 'Course',  'CourseProfessor',
        function($scope, Course, CourseProfessor) {

            $scope.courseId = /course\/([^\/]+)\/permissions/.extract(location.pathname, 1);
            $scope.professors = CourseProfessor.query({course: $scope.courseId});
            $scope.remove_professor = function(course_professor_id, index) {
                    if(!confirm('Tem certeza que deseja remover este professor deste curso?')) return;
                    var bla = 1;
                    CourseProfessor.remove({id: course_professor_id}, function (){
                        $scope.professors.splice(index, 1);
                    });
                };
        }
    ]);

})(angular);
