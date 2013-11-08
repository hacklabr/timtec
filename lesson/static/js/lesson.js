/** TODO: initialize this in proprer way (fabio) */
function initialize_code_mirror($scope, data, expected) {
    var body = $('#empty').contents().find('body');
    var cm = CodeMirror.fromTextArea($('#texto')[0], CodeMirrorConf);
    cm.setSize("100%", "215px"); // TODO: set size in html
    cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
    cm.markText({line:4, ch:1000}, {line:7, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});
    cm.replaceRange(data, {line:4, ch:0}, {line:4, ch:100});
    setTimeout(function () {
        $('#empty').contents().find('body').html(cm.getValue());
        $('#expected_iframe').contents().find('body').html('' + expected);
    }, 800);
    cm.on('change', function (instance) {
        data = instance.getValue();
        $('#empty').contents().find('body').html(data);
        $scope.answer.given = data;
    });
}

(function (angular) {
    "use strict";

    var app = angular.module('lesson', ['ngRoute', 'ngResource', 'youtube', 'forum']);

    var ACTIVITY_TEMPLATE_PATH = function(the_type){
        return STATIC_URL + '/templates/activity_'+ the_type + '.html';
    };

    app.config(['$routeProvider', '$httpProvider',
        function ($routeProvider, $httpProvider) {
            $routeProvider
                .when('/:unitPos', {
                    templateUrl: STATIC_URL + '/templates/lesson_video.html',
                    controller: 'LessonVideoCtrl'})
                .when('/:unitPos/activity', {
                    templateUrl: STATIC_URL + '/templates/lesson_activity.html',
                    controller: 'LessonActivityCtrl'})
                .otherwise({redirectTo: '/1'});

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);

    app.controller('LessonMainCtrl', ['$scope', 'LessonData',
        function ($scope, LessonData) {
            $scope.currentUnitPos = parseInt( /#\/(\d+)/.extract(location.hash, 1), 10);
            $scope.currentUnitPos = Math.max($scope.currentUnitPos, 1);

            $scope.isSelected = function(i){
                return ($scope.currentUnitPos-1) === i;
            };
            $scope.isDone = function(unit){
                return (unit.progress || {}).complete;
            };
            $scope.select = function(i) {
                $scope.currentUnitPos = i+1;
            };
        }
    ]);

    app.controller('LessonActivityCtrl', ['$scope', '$location', '$routeParams', '$http', 'LessonData',
        function ($scope, $location, $routeParams, $http, LessonData) {
            var $main = $scope.$parent;

            $scope.alternatives = [];
            $scope.currentUnitIndex = $main.currentUnitPos - 1;
            $scope.answer = {'given': null};
            $scope.sendOrNextText = 'Enviar';

            $scope.nextVideo = function() {
                $main.currentUnitPos++;
                $location.path('/' + $main.currentUnitPos);
            };
            $scope.replayVideo = function() {
                $location.path('/'+$main.currentUnitPos);
            };

            $scope.sendOrNext = function() {
                if ($scope.correct) {
                    $scope.nextVideo();
                } else {
                    $scope.sendAnswer();
                }
            };

            $scope.sendAnswer = function() {
                function tellResult(data) {
                    var correct = data.correct,
                        given  = data.given,
                        expected  = data.expected;

                    if(correct){
                        _gaq.push(['_trackEvent', 'Atividades', 'Resultado', 'Ok']);
                        $scope.currentUnit.progress = {complete : true};
                        $scope.correct = true;
                        $scope.sendOrNextText = "Continuar";
                    } else {
                        _gaq.push(['_trackEvent', 'Atividades', 'Resultado', 'Falso']);
                    }

                    $scope.isCorrect = correct;
                }

                _gaq.push(['_trackEvent', 'Atividades', 'Enviar']);

                $http({
                    'method': 'POST',
                    'url': '/api/answer/' + $scope.currentUnitId,
                    'data': 'given=' + JSON.stringify($scope.answer.given),
                    'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(tellResult);
            };

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit = lesson.units[$scope.currentUnitIndex];
                $scope.currentUnitId = unit.id;
                $scope.activity_template = unit.activity.template;

                if (unit.activity.data.alternatives) {
                    $scope.alternatives = unit.activity.data.alternatives.map(
                        function(a,i) { return {'title': a }; }
                    );
                }

                if (unit.activity.type == 'multiplechoice') {
                    $scope.answer.given = $scope.alternatives.map(
                        function(a,i){ return false; }
                    );
                } else if (unit.activity.type == 'trueorfalse') {
                    $scope.answer.given = $scope.alternatives.map(
                        function(a,i){ return null; }
                    );
                } else if(unit.activity.type === 'relationship') {
                    $scope.answer.given = unit.activity.data.column1.map(
                        function(a,i){ return null; }
                    );
                } else if(unit.activity.type === 'html5') {
                    /** TODO: initialize this in proprer way (fabio) */
                    setTimeout(function () {
                        initialize_code_mirror($scope, unit.activity.data.data, unit.activity.expected.expected_answer);
                    }, 100);
                }

            });
        }
    ]);


    app.controller('LessonVideoCtrl', ['$scope', '$http', '$location', 'LessonData', 'youtubePlayerApi',
        function ($scope, $http, $location, LessonData, youtubePlayerApi) {
            var $main = $scope.$parent;
            var currentUnitIndex = $main.currentUnitPos - 1;

            var onPlayerStateChange = function (event) {
                if (event.data === YT.PlayerState.ENDED) {
                    if( $scope.currentUnit.activity ) {
                        $location.path('/' + $main.currentUnitPos + '/activity');
                    } else {
                        if ($main.currentUnitPos + 1 < $scope.lesson.units.length) {
                            $main.currentUnitPos++;
                            $location.path('/' + $main.currentUnitPos);
                        }
                    }

                    $http({
                        'method': 'POST',
                        'url': '/api/updatestudentprogress/' + $scope.currentUnitId,
                        'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                    }).success(function(data){
                        $scope.currentUnit.progress = {complete: data.complete};
                    });
                    $scope.$apply();
                }
            };

            LessonData.then(function (lesson) {
                $scope.currentUnit = lesson.units[(currentUnitIndex || 0)];
                $scope.currentUnitId = $scope.currentUnit.id;

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
            var Progress = $resource('/api/student_progress?unit__lesson=:lessonId');
            var deferred = $q.defer();

            Lesson.get({'lessonId': $window.lessonId}, function (lesson) {
                lesson.units.forEach(function(unit, index){
                    if(unit.activity) {
                        unit.activity.template = ACTIVITY_TEMPLATE_PATH(unit.activity.type);
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

    app.directive('radio', function () {
        return function (scope, element) {
            $(element).radio();
        };
    });

    app.directive('checkbox', function () {
        return function (scope, element) {
            $(element).checkbox();
        };
    });


})(angular);
