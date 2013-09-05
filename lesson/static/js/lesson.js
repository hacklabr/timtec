(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute']);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/:unitID', {
                templateUrl: 'lesson_internal.html',
                controller: 'LessonCtrl'})
            .otherwise({redirectTo: '/0'});
    }]);

    app.controller('LessonCtrl', function ($scope, $routeParams) {
        $scope.units = [1, 2, 3];
        $scope.unitID = parseInt($routeParams.unitID, 10);
    });
})(angular);
