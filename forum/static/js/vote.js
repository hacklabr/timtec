(function (angular) {
    "use strict";
    console.log('App vote!!!!');
    var app = angular.module('timtecVote', ['ngRoute', 'ngResource', "ngCookies", ]);

    // Uses the csrftoken from the cookie
    app.run(function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });
    // Avoid jumping to top after click in anchor '#'
    app.value('$anchorScroll', angular.noop);

    app.controller('QuestionVoteCtrl', ['$scope', '$window', 'QuestionVote',
        function ($scope, $window, QuestionVote) {
            $scope.questionId = parseInt($window.question_id, 10);
            // Verify if user has voted in up or down
            $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_up = '';
                        $scope.user_question_vote_down = '';
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = 'active';  
                        $scope.user_question_vote_down = '';
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_up = '';
                        $scope.user_question_vote_down = 'active';
                    }
            });
            $scope.voteUp = function() {
                $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                    if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_up = 'active';  
                        $scope.question_votes += 1;
                        question_vote.value = 1;
                        question_vote.$update({question: $scope.questionId});
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';  
                        $scope.question_votes -= 1;
                        question_vote.value = 0;
                        question_vote.$update({question: $scope.questionId});
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_up = 'active';
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 2;
                        question_vote.value = 1;
                        question_vote.$update({question: $scope.questionId});
                    }
                });
            };
            $scope.voteDown = function() {
                $scope.question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                    if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 1;
                        question_vote.value = -1;
                        question_vote.$update({question: $scope.questionId});
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 2;
                        question_vote.value = -1;
                        question_vote.$update({question: $scope.questionId});
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 1;
                        question_vote.value = 0;
                        question_vote.$update({question: $scope.questionId});
                    }
                });
            };

    }]);
// 
    // app.factory('AnswerVote', function($resource){
        // return $resource('/api/answer_vote/', {}, {
            // create: {method: 'POST'}
        // });
    // });
    app.factory('QuestionVote', function($resource){
        return $resource('/api/question_vote/:question', {}, {
            get: {method: 'GET'},
            update: {method: 'PUT'},
        });
    });

})(angular);