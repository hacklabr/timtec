(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController', ['$scope', 'Course',
        function($scope, Course) {
            $scope.course = new Course();
            $scope.errors = {};

            $scope.saveCourse = function() {
                $scope.course.$save().catch(function(response){
                    $scope.errors = response.data;
                });
            };
        }
    ]);

})(window.angular);