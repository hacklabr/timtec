(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', []);

    app.controller('PHPCtrl', ['$scope', '$sce', 'Progress',
        function ($scope, $sce, Progress) {

            $scope.disableResultTab = true;
            $scope.cm_refresh = 0;
            $scope.iframeRefresh = 0;

            $scope.refresh  = function() {
                $scope.cm_refresh += 1;
            };

            $scope.answer.$promise.finally(function() {
                if (!$scope.answer.id) {
                    $scope.answer.given = $scope.currentActivity.data;
                }
                $scope.answer.given[0].active = true;
                $scope.refresh();
            });

             $scope.sendPhpAnswer = function() {
                 $scope.answer.activity = $scope.currentActivity.id;
                 $scope.answer.$update({activityId: $scope.answer.activity}, function () {
                     $scope.disableResultTab = false;
                     $scope.resultUrl = $sce.trustAsResourceUrl('http://php' + $scope.answer.user_id + '.timtec.com.br/');
                     $scope.iframeRefresh += 1;
                 }).then(function(d){
//                    ga('send', 'event', 'activity', 'result', '', d.correct);
                     return Progress.getProgressByUnitId($scope.currentUnit.id);
                 }).then(function(progress){
                     $scope.currentUnit.progress = progress;
                 });
//                ga('send', 'event', 'activity', 'submit');

            };

            $scope.codemirrorLoaded = function(cm){
                // FIXME refactor this.
                var pid = setInterval(function(){
                    if ($scope.cm_refresh < 20) {
                        $scope.refresh();
                    } else
                        clearInterval(pid);
                }, 500);
            };

            $scope.codemirrorConfig = {
                        lineNumbers:true,
                        theme:'monokai',
                        matchTags: {bothTags: true},
                        matchBrackets: true,
                        extraKeys: {'Ctrl-J': 'toMatchingTag',
                                    'Ctrl-Space': 'autocomplete'},
                        mode:'php',
                        onLoad : $scope.codemirrorLoaded
            };
        }
    ]);

    app.controller('RelationshipCtrl', ['$scope',
        function ($scope) {

            function compareNumbers(a, b) {
              return a - b;
            }

            $scope.$watch('currentActivity', function(currentActivity) {
                $scope.possibleAnswers = currentActivity.expected.slice(0);
                $scope.possibleAnswers.sort(compareNumbers);
            });

            $scope.possibleAnswers = $scope.currentActivity.expected.slice(0);
            $scope.possibleAnswers.sort(compareNumbers);
        }
    ]);
})(angular);
