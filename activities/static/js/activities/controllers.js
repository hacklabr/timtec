(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', ['ngSanitize']);

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

    app.controller('DiscussionActivityCtrl', [
      '$scope',
      '$sce',
      '$routeParams',
      'uiTinymceConfig',
      'Forum',
      'Topic',
      'Comment',
      'TopicLike',
      'CommentLike',
      'CommentFile',

      function ($scope, $sce, $routeParams, uiTinymceConfig, Forum, Topic, Comment, TopicLike, CommentLike, CommentFile) {
        $scope.activity_open = true;
        $scope.activity_expired = false;
        var now = Date.now();
        console.log("oiii");
        
        // Decide the current state of the activity
        if(now < $scope.currentActivity.data[0].start_date){
          // The Activity is not open yet
          $scope.activity_open = false;
        } else if(now > $scope.currentActivity.data[0].end_date){
          // The Activity is already expired
          $scope.activity_expired = true;
        }

        // check if there is already an answer from this user
        $scope.answer.$promise.finally(function() {
            if (!$scope.answer.id) {
                $scope.answer.given = $scope.currentActivity.data;
            }
            $scope.answer.given[0].active = true;
            $scope.refresh();
        });

        // if there is, show the corresponding topic that holds this answer and its comments

        // if there is no answer, show the text editor and prepare to save it
        $scope.forums = Forum.query();
        $scope.new_topic = new Topic();
        $scope.save_answer = function() {
            $scope.sending = true;
            // $scope.new_topic.forum = 1;
            $scope.new_topic.$save(function(topic){
                $scope.answer = {};
                $scope.answer.given = {topic: topic.id};
                $scope.answer.$save();
            });
        };




      }
    ]);
})(angular);
