(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', ['ui.codemirror', 'lesson.services']);

    app.controller('LessonActivityCtrl',
        function ($scope, $location, $routeParams, $http, LessonData, Answer, $q, resolveActivityTemplate) {
            var $main = $scope.$parent;

            $main.currentUnitPos = parseInt($routeParams.unitPos, 10);

            $scope.alternatives = [];
            console.log($scope.answer);
            // $scope.answer = {given: null, correct: null};

            $scope.nextVideo = function() {
                if ($main.currentUnitPos + 1 <= $scope.lesson.units.length) {
                    $main.currentUnitPos++;
                    $location.path('/' + $main.currentUnitPos).search('autoplay', null);
                }
            };
            $scope.replayVideo = function() {
                $location.path('/' + $main.currentUnitPos).search('autoplay', 1);
            };

            $scope.sendAnswer = function() {
                var answer = new Answer({'given': $scope.answer.given});
                answer.unit = $scope.currentUnit.id;
                answer.activity = $scope.currentUnit.activity.id;
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

            $scope.emptyLoaded = $q.defer();
            window.onLoadEmpty = function () {
                $scope.$apply(function () {
                    $scope.emptyLoaded.resolve();
                });
            };

            LessonData.then(function (lesson) {
                var unit = $scope.currentUnit = lesson.units[$main.currentUnitPos - 1];
                $scope.currentUnitId = unit.id;
                $scope.activity_template = resolveActivityTemplate(unit.activity.type);

                if (unit.activity.data.alternatives) {
                    $scope.alternatives = unit.activity.data.alternatives.map(
                        function(a,i) { return {'title': a }; }
                    );
                }

                if(unit.activity.id) {
                    var extractLatest = function (list) {
                        if(list.length > 0) {
                            $scope.answer = list.pop();
                            if(unit.activity.type === "html5")
                                $scope.loadedAnswer = $scope.answer;
                        }
                    };
                    Answer.query({'activity': unit.activity.id}, extractLatest);
                }

                if( !$scope.answer.given ) {
                    if (unit.activity.type === 'multiplechoice') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return false; }
                        );
                    } else if (unit.activity.type === 'trueorfalse') {
                        $scope.answer.given = $scope.alternatives.map(
                            function(a,i){ return null; }
                        );
                    } else if(unit.activity.type === 'relationship') {
                        $scope.answer.given = unit.activity.data.column1.map(
                            function(a,i){ return null; }
                        );
                    }
                }
            });
        }
    );

    app.controller('HTML5Ctrl',
        function ($scope) {
            if( !$scope.answer.given ) {
                var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
                var atemplate = "\n  </body>\n</html>";
                $scope.answer.given = [btemplate + unit.activity.data.data + atemplate];
            }

            $scope.codemirrorLoaded = function(cm){

                cm.on("change", function() {
                    cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
                    var lastLine = cm.lineCount();
                    alert(lastLine);
                    cm.markText({line:lastLine-3, ch:1000}, {line:lastLine, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});

                });
              };
        }
    );

})(window.angular);
