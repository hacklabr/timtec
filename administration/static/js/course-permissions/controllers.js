(function(angular){

    angular.module('course-permissions.controllers', []).
        controller('PermissionsController', ['$scope', '$modal', '$http', 'Course',  'CourseProfessor',
        function($scope, $modal, $http, Course, CourseProfessor) {

            $scope.courseId = /course\/([^\/]+)\/permissions/.extract(location.pathname, 1);
            $scope.professors = CourseProfessor.query({course: $scope.courseId, has_user: true});
            $scope.remove_professor = function(course_professor_id, index) {
                if(!confirm('Tem certeza que deseja remover este professor deste curso?')) return;
                CourseProfessor.remove({id: course_professor_id}, function (){
                    $scope.professors.splice(index, 1);
                });
            };

            $scope.update_professor_role = function(professor){
                professor.$update({id: professor.id});
            };

            $scope.new_professors = function () {
                var modalInstance = $modal.open({
                    templateUrl: 'newProfessorModal.html',
                    controller: ['$scope', '$modalInstance', 'course_id', addProfessorsModalInstanceCtrl],
                    resolve: {
                        course_id: function () {
                            return $scope.course_id;
                        }
                    }
                });
                modalInstance.result.then(function (new_professors) {
                    angular.forEach(new_professors, function(professor){
                        var new_professor = CourseProfessor.save({course: $scope.courseId, user: professor.id});
                        $scope.professors.unshift(new_professor);
                    });
                });
            };
            var addProfessorsModalInstanceCtrl = function ($scope, $modalInstance, course_id) {

                $scope.new_professors = [];
                $scope.add_professors = function () {
                    $modalInstance.close($scope.new_professors);
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };

                $scope.on_select_professor = function(model) {
                    $scope.new_professors.unshift(model);
                    $scope.asyncSelected = '';
                };

                $scope.remove_new_professor = function(index) {
                    $scope.new_professors.splice(index, 1);
                };

                $scope.getUsers = function(val) {
                    return $http.get('/api/user_search', {
                        params: {
                          name: val,
                          sensor: false
                        }
                    }).then(function(res){
                        var professors_found = [];
                        angular.forEach(res.data, function(item){
                            var formated_name = '';
                            if (item.first_name)
                                formated_name += item.first_name;
                            if (item.last_name)
                                formated_name = formated_name + ' ' + item.last_name;
                            if (formated_name)
                                formated_name = formated_name + ' - ';
                            formated_name += item.username;
                            if (item.email)
                                formated_name = formated_name + ' - ' + item.email;
                            item.formated_name = formated_name;
                            professors_found.push(item);
                        });
                        return professors_found;
                    });
                };
            };
        }
    ]);

})(angular);
