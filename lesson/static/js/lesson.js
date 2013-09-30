(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube']);

    var ACTIVITY_TEMPLATE_PATH = function(the_type){
        return STATIC_URL + '/templates/activity_'+ the_type + '.html';
    };

    app.config(['$routeProvider', '$httpProvider',
        function ($routeProvider, $httpProvider) {
            $routeProvider
                .when('/:unitPos', {
                    templateUrl: STATIC_URL + '/templates/lesson_video.html',
                    controller: 'LessonVideo'})
                .when('/:unitPos/activity', {
                    templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                    controller: 'LessonActivity'})
                .otherwise({redirectTo: '/0'});

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);

    app.controller('LessonActivity', ['$scope', '$routeParams', '$http', 'LessonData',
        function ($scope, $routeParams, $http, LessonData) {
            $scope.alternatives = [];
            $scope.currentUnitPos = parseInt($routeParams.unitPos, 10);
            $scope.answer = {'given': null};

            $scope.sendAnswer = (function() {
                function tellResult(data) {
                    var correct = data.correct,
                        given  = data.given,
                        expected  = data.expected;

                    if (given['forEach']) {
                        given.forEach(function(g, i){
                            $scope.alternatives[i].eval = (g === expected[i] ? 'correct' : 'wrong');
                            console.log($scope.alternatives[i].eval);
                        });
                    } else {
                        $scope.alternatives[given].eval = correct ? 'correct' : 'wrong';
                    }
                }

                $http({
                    'method': 'POST',
                    'url': '/api/answer/' + $scope.currentUnitId,
                    'data': 'given=' + JSON.stringify($scope.answer.given),
                    'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(tellResult);
            });

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit = lesson.units[$scope.currentUnitPos];
                $scope.currentUnitId = unit.id;
                $scope.activity_template = unit.activity.template;
                $scope.alternatives = unit.activity.alternatives.map(
                    function(a,i) { return {'title': a }; }
                );

                if (['multiplechoice','trueorfalse'].indexOf(unit.activity.type) >= 0) {
                    $scope.answer.given = $scope.alternatives.map(
                        function(a,i){ return false; }
                    );
                }

            });
        }
    ]);


    app.controller('LessonVideo', ['$scope', '$routeParams', '$location', 'LessonData', 'youtubePlayerApi',
        function ($scope, $routeParams, $location, LessonData, youtubePlayerApi) {
            $scope.currentUnitPos = parseInt($routeParams.unitPos, 10);
            window.ypa = youtubePlayerApi;

            var onPlayerStateChange = function (event) {
                if (event.data === YT.PlayerState.ENDED) {
                    if( $scope.currentUnit.activity ) {
                        $location.path('/' + $scope.currentUnitPos + '/activity');
                    } else {
                        var nextId = $scope.currentUnitPos + 1;
                        if (nextId < $scope.lesson.units.length) {
                            $location.path('/' + nextId);
                        }
                    }
                    $scope.$apply();
                }
            };

            LessonData.then(function (lesson) {
                $scope.currentUnit = lesson.units[$scope.currentUnitPos];
                $scope.currentUnitId = $scope.currentUnit.id;

                if ($scope.currentUnit.video) {
                    youtubePlayerApi.videoId = $scope.currentUnit.video.youtube_id;
                    youtubePlayerApi.events = {
                        onStateChange: onPlayerStateChange
                    };
                    youtubePlayerApi.loadPlayer();
                    if( ! youtubePlayerApi.player ) {
                        youtubePlayerApi.deffered.resolve();
                    }
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
                        var type = unit.activity.type;
                        unit.activity = JSON.parse(unit.activity.data);
                        // TODO: corrigir após definição exata do dado (fabio)
                        if(unit.activity.length > 0) {
                            unit.activity = unit.activity.pop();
                        }
                        // TODO: delegar esta estruturação ao django (fabio)
                        unit.activity.type = type;
                        unit.activity.template = ACTIVITY_TEMPLATE_PATH(type);
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
