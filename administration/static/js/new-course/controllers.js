(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController', ['$scope',
        function($scope) {
            $scope.al = function(){ console.log('saved'); throw Error('merda'); };
            $scope.course = {};
            $scope.course.name = 'html';
            $scope.course.abstract = 'Isso é um **teste** do editor.';
        }
    ]);

})(window.angular);