(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube']);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/:unitId', {
                templateUrl: 'lesson_internal.html',
                controller: 'LessonCtrl'})
            .otherwise({redirectTo: '/0'});
    }]);

    app.controller('LessonCtrl', function ($scope, $routeParams, LessonData, youtubePlayerApi) {
        $scope.currentUnitId = parseInt($routeParams.unitId, 10);
        LessonData.then(function (lesson) {
            $scope.currentUnit = lesson.units[$scope.currentUnitId];
            if ($scope.currentUnit.video) {
                youtubePlayerApi.videoId = $scope.currentUnit.video.youtube_id;
                youtubePlayerApi.loadPlayer();
            }
        });
    });

    app.factory('LessonData', function($rootScope, $q, $resource, $window) {
        var Lesson = $resource('/api/lessons/:lessonId/');
        var deferred = $q.defer();
        Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
            $rootScope.lesson = lesson;
            deferred.resolve(lesson);
        });

        return deferred.promise;
    });
})(angular);
