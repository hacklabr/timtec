(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController', ['$scope', 'course',
        function($scope, course) {
            $scope.course = course;
        }
    ]);

})(window.angular);