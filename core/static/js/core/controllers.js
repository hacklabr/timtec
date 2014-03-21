(function(angular){
    'use strict';

    var app = angular.module('core.controllers', []);

    app.controller('HomeCtrl', ['$scope', 'Course',
        function ($scope, Course) {
            $scope.courses = Course.query({home_published: true});
        }
    ]);

})(angular);
