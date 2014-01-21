(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', ['ui.codemirror', 'lesson.services']);

    app.controller('LessonActivityCtrl',
        function ($scope, $location, $routeParams, $http, LessonData, Answer, $q, resolveActivityTemplate) {
            $scope.alternatives = [];
            $scope.answer = {given: null, correct: null};

            $scope.nextVideo = function() {
                $scope.gotoNexUnit(false);
            };
            $scope.replayVideo = function() {
                $location.path('/' + $main.currentUnitPos).search('autoplay', 1);
            };

            $scope.sendAnswer = function() {
                var answer = new Answer({'given': $scope.answer.given});
                answer.unit = $scope.currentUnit.id;
                answer.activity = $scope.activity.id;
                delete answer.id;
                answer.$save().then(function(d){
                    ga('send', 'event', 'activity', 'result', '', d.correct);
                    $scope.answer.correct = d.correct;
                    if (d.correct) {
                        $http({
                            'method': 'POST',
                            'url': '/api/updatestudentprogress/' + $scope.currentUnitId + '/',
                            'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
                        }).success(function(data){
                            $scope.currentUnit.progress = {complete: data.complete};
                            if (data.complete) {
                                ga("send", "event", "unit", "unit completed");
                            }
                        });
                    }
                });
                ga('send', 'event', 'activity', 'submit');
            };

            $scope.loadActivity = function () {
                $scope.activity_template = resolveActivityTemplate(unit.activity.type);
            }

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit;
                $scope.activity = unit.activity

                $scope.recAnswer = $q.defer();
                function return_last (answers) {
                    if (answers.length > 0) {
                        $scope.answer = answers.pop()
                        return $scope.recAnswer.resolve($scope.answer);
                    } else {
                        $scope.recAnswer.reject('Nenhuma resposta');
                    }
                }
                Answer.query({'activity': $scope.activity.id}, return_last);

                if ($scope.activity.data.alternatives) {
                    $scope.alternatives = $scope.activity.data.alternatives.map(
                        function(a,i) { return {'title': a }; }
                    );
                }
                console.log($scope.recAnswer);
                $scope.recAnswer.promise.then(function () {
                    $scope.loadActivity()
                }, function (reason) {
                    $scope.loadActivity()
                    if ($scope.activity.type === 'multiplechoice') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return false; }
                        );
                    } else if ($scope.activity.type === 'trueorfalse') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return null; }
                        );
                    } else if($scope.activity.type === 'relationship') {
                        $scope.answer.given = $scope.activity.data.column1.map(
                            function(a,i){ return null; }
                        );
                    }
                });
            });
        }
    );

    app.controller('HTML5Ctrl',
        function ($scope) {
            if( !$scope.answer.given ) {
                var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
                var atemplate = "\n  </body>\n</html>";
                $scope.answer.given = [btemplate + $scope.activity.data.data + atemplate];
            }

            $scope.codemirrorLoaded = function(cm){
                cm.on("change", function() {
                    cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
                    var lastLine = cm.lineCount();
                    cm.markText({line:lastLine-3, ch:1000}, {line:lastLine, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});
                });
            };
        }
    );

})(window.angular);
