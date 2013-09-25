(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube']);

    app.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
            .when('/:unitId', {
                templateUrl: STATIC_URL + '/templates/lesson_video.html',
                controller: 'LessonVideo'})
            .when('/:unitId/activity', {
                templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                controller: 'LessonActivity'})
            .otherwise({redirectTo: '/0'});
    }]);

    app.controller('LessonActivity', ['$scope', '$routeParams', '$location', '$resource', 'LessonData',
        function ($scope, $routeParams, $location, $resource, LessonData) {
            $scope.currentUnitId = parseInt($routeParams.unitId, 10);


            $scope.sendAnswer = (function() {
                var answers = Array.prototype.map.call(
                    angular.element('.activity .answers input'),
                    function(el){ return el.checked; }
                );
            });

            LessonData.then(function (lesson) {
                $scope.currentUnit = lesson.units[$scope.currentUnitId];
            });
        }
    ]);


    app.controller('LessonVideo', ['$scope', '$routeParams', '$location', 'LessonData', 'youtubePlayerApi',
        function ($scope, $routeParams, $location, LessonData, youtubePlayerApi) {
            $scope.currentUnitId = parseInt($routeParams.unitId, 10);

            var onPlayerStateChange = function (event) {
                if (event.data === YT.PlayerState.ENDED) {
                    console.log('/' + $scope.currentUnitId + '/activity');
                    if( $scope.currentUnit.activity ) {
                        $location.path('/' + $scope.currentUnitId + '/activity');
                    } else {
                        var nextId = $scope.currentUnitId + 1;
                        if (nextId < $scope.lesson.units.length) {
                            $location.path('/' + nextId);
                        }
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
        }
    ]);

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window',
        function($rootScope, $q, $resource, $window) {
            var Lesson = $resource('/api/lessons/:lessonId/');
            var Progress = $resource('/api/student_progress/?unit__lesson=:lessonId');
            var deferred = $q.defer();

            Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
                lesson.units.forEach(function(unit, index){
                    if(unit.activity) {
                        unit.activity = JSON.parse(unit.activity.data);
                        // TODO: corrigir após definição exata do dado (fabio)
                        if(unit.activity.length > 0) {
                            unit.activity = unit.activity.pop();
                        }
                    }
                });
                $rootScope.lesson = lesson;
                deferred.resolve(lesson);
            });

            Progress.query({'lessonId': $window.lessonId}, function (progress) {
                deferred.promise.then(function (lesson) {
                    for (var i = progress.length - 1; i >= 0; i--) {
                        var p = progress[i];
                        for (var j = lesson.units.length - 1; j >= 0; j--) {
                            if (lesson.units[j].id === p.unit) {
                                lesson.units[j].progress = p;
                            }
                        }
                    }
                });
            });

            return deferred.promise;
        }
    ]);
})(angular);
