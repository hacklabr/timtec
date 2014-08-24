(function(angular){

    angular.module('course-permissions.controllers', []).
        controller('PermissionsController', ['$scope', '$modal', '$http', 'Course',  'CourseProfessor',
        function($scope, $modal, $http, Course, CourseProfessor) {

            $scope.courseId = /course\/([^\/]+)\/permissions/.extract(location.pathname, 1);
            $scope.professors = CourseProfessor.query({course: $scope.courseId});
            $scope.remove_professor = function(course_professor_id, index) {
                    if(!confirm('Tem certeza que deseja remover este professor deste curso?')) return;
                    var bla = 1;
                    CourseProfessor.remove({id: course_professor_id}, function (){
                        $scope.professors.splice(index, 1);
                    });
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
//                    new_message.$save({}, function(new_message){
//                        $scope.messages.unshift(new_message);
//                    });

                });
            };
            var addProfessorsModalInstanceCtrl = function ($scope, $modalInstance, course_id) {

                $scope.send = function () {
//                    $modalInstance.close($scope.new_message);
                    $modalInstance.close();
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss();
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
                            professors_found.push(formated_name);
                        });
                        return professors_found;
                    });
                };
            };
        }
    ]);

})(angular);
