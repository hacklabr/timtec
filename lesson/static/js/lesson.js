(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource']);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/:unitId', {
                templateUrl: 'lesson_internal.html',
                controller: 'LessonCtrl'})
            .otherwise({redirectTo: '/0'});
    }]);

    app.controller('LessonCtrl', function ($rootScope, $scope, $routeParams, LessonData, $window) {
        $scope.currentUnitId = parseInt($routeParams.unitId, 10);
        LessonData.get({'lessonId': $window.lessonId}, function (lesson) {
            $scope.lesson = lesson;
            $scope.currentUnit = lesson.units[$scope.currentUnitID];
        });
    });

    app.factory('LessonData', function($resource) {
        return $resource('/api/lessons/:lessonId');
    });
})(angular);
