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

        // Decide the current state of the activity
        if(now < $scope.currentActivity.data[0].start_date){
          // The Activity is not open yet
          $scope.activity_open = false;
        } else if(now > $scope.currentActivity.data[0].end_date){
          // The Activity is already expired
          $scope.activity_expired = true;
        }

        // Check if there is an answer to this activity
        $scope.answer.$promise.then(function() {
            // if there is, show the corresponding topic that holds this answer and its comments
            $scope.topic = Topic.get({id: $scope.answer.given.topic});
            uiTinymceConfig.automatic_uploads = true;
        });

        // if there is no answer, show the text editor and prepare to save it
        // $scope.forums = Forum.query();
        $scope.new_topic = new Topic();
        $scope.save_answer = function() {
            // $scope.sending = true;
            $scope.new_topic.forum = 14;
            $scope.new_topic.title = 'Título experimental';
            $scope.new_topic.$save(function(topic){
                $scope.answer.given = {topic: topic.id};
                $scope.answer.activity = $scope.currentActivity.id;
                $scope.answer.$save();
            });
        };

        $scope.save_comment = function(topic, parent_comment) {
            var new_comment = new Comment();
            var new_comment_files = [];
            new_comment.topic = topic.id;
            if (parent_comment) {
                new_comment.parent = parent_comment.id;
                new_comment.text = parent_comment.new_comment;
                new_comment_files = parent_comment.new_comment_files;
                parent_comment.comment_replies.unshift(new_comment);
            } else {
                new_comment.text = topic.new_comment;
                topic.show_comment_input = false;
                new_comment_files = topic.new_comment_files;
                topic.comments.unshift(new_comment);
            }
            new_comment.$save().then(function(comment) {
                angular.forEach(new_comment_files, function(comment_file) {
                    comment_file.comment = comment.id;
                    delete comment_file.file;
                    comment_file.$patch().then(function(comment_file_complete) {
                        comment.files.push(comment_file_complete);
                    });
                })
            });
        };




      }
    ]);
})(angular);
