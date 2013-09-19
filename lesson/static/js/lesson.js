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

    app.controller('LessonCtrl', ['$scope', '$routeParams', '$location', 'LessonData', 'youtubePlayerApi',
        function ($scope, $routeParams, $location, LessonData, youtubePlayerApi) {
        $scope.currentUnitId = parseInt($routeParams.unitId, 10);

        var onPlayerStateChange = function (event) {
            if (event.data === YT.PlayerState.ENDED) {
                console.log('carregando próximo');
                console.log($location.path());
                var nextId = $scope.currentUnitId + 1;
                if (nextId < $scope.lesson.units.length) {
                    $location.path('/' + nextId);
                }
                $scope.$apply();
            }
        };

        LessonData.then(function (lesson) {
            $scope.currentUnit = lesson.units[$scope.currentUnitId];
            if ($scope.currentUnit.video) {
                youtubePlayerApi.videoId = $scope.currentUnit.video.youtube_id;
                youtubePlayerApi.events = {
                    onStateChange: onPlayerStateChange
                };
                youtubePlayerApi.loadPlayer();
            }
        });
    }]);

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window',
        function($rootScope, $q, $resource, $window) {
        var Lesson = $resource('/api/lessons/:lessonId/');
        var deferred = $q.defer();
        Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
            $rootScope.lesson = lesson;
            deferred.resolve(lesson);
        });
        return deferred.promise;
    }]);
})(angular);
