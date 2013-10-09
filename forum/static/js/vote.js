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
                var question_vote = QuestionVote.get({question: $scope.questionId}, function (question_vote){
                    if ((question_vote.value == undefined) || (question_vote.value == 0)){
                        $scope.user_question_vote_up = 'active';  
                        $scope.question_votes += 1;
                        question_vote.value = 1;
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';  
                        $scope.question_votes -= 1;
                        question_vote.value = 0;
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_up = 'active';
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 2;
                        question_vote.value = 1;
                    }
                    question_vote.$update({question: $scope.questionId});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        question_vote.question = $scope.questionId;
                        $scope.user_question_vote_up = 'active';  
                        $scope.question_votes += 1;
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
                    } else if (question_vote.value == 1) {
                        $scope.user_question_vote_up = '';
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 2;
                        question_vote.value = -1;
                    } else if (question_vote.value == -1) {
                        $scope.user_question_vote_down = '';
                        $scope.question_votes += 1;
                        question_vote.value = 0;
                    }
                    question_vote.$update({question: $scope.questionId});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        question_vote.question = $scope.questionId;
                        $scope.user_question_vote_down = 'active';
                        $scope.question_votes -= 1;
                        question_vote.value = -1;
                        question_vote.$update({question: $scope.questionId});
                    }
                });
            };
    }]);

    app.controller('AnswerVoteCtrl', ['$scope', '$window', 'AnswerVote',
        function ($scope, $window, AnswerVote) {
            // Verify if user has voted in up or down for this answer
            $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id}, 
                function (answer_vote){
                    if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = '';
                    } else if (answer_vote.value == 1) {
                        $scope.user_answer_vote_up = 'active';  
                        $scope.user_answer_vote_down = '';
                    } else if (answer_vote.value == -1) {
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = 'active';
                    }
                    $scope.answer.votes = answer_vote.value;
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        $scope.answer.votes = 0;
                    }
                });
            $scope.voteUp = function(index) {
                $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id}, 
                    function(answer_vote) {
                        if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                            answer_vote.answer = $scope.answer.id;
                            answer_vote.value = 1;
                            $scope.user_answer_vote_up = 'active';  
                            $scope.answer.votes += 1;
                        } else if (answer_vote.value == 1) {
                            $scope.user_answer_vote_up = '';  
                            $scope.answer.votes -= 1;
                            answer_vote.value = 0;
                        } else if (answer_vote.value == -1) {
                            $scope.user_answer_vote_up = 'active';
                            $scope.user_answer_vote_down = '';
                            $scope.answer.votes += 2;
                            answer_vote.value = 1;
                        }
                        answer_vote.$update({answer: answer_vote.answer});
                    },
                    function (httpResponse){
                        if (httpResponse.status == 404) {
                            var new_answer_vote = new AnswerVote();
                            new_answer_vote.answer = $scope.answer.id;
                            new_answer_vote.value = 1;
                            new_answer_vote.$update({answer: new_answer_vote.answer});
                            $scope.user_answer_vote_up = 'active';  
                            $scope.answer.votes += 1;
                    }
                });
            };
            $scope.voteDown = function(index) {
                $scope.answer_vote = AnswerVote.get({answer: $scope.answer.id}, function(answer_vote) {
                    if ((answer_vote.value == undefined) || (answer_vote.value == 0)){
                        $scope.user_answer_vote_down = 'active';
                        $scope.answer.votes -= 1;
                        answer_vote.value = -1;
                    } else if (answer_vote.value == 1) {
                        $scope.user_answer_vote_up = '';
                        $scope.user_answer_vote_down = 'active';
                        $scope.answer.votes -= 2;
                        answer_vote.value = -1;
                    } else if (answer_vote.value == -1) {
                        $scope.user_answer_vote_down = '';
                        $scope.answer.votes += 1;
                        answer_vote.value = 0;
                    }
                    answer_vote.$update({answer: answer_vote.answer});
                },
                function (httpResponse){
                    if (httpResponse.status == 404) {
                        var new_answer_vote = new AnswerVote();
                        new_answer_vote.answer = $scope.answer.id;
                        new_answer_vote.value = -1;
                        new_answer_vote.$update({answer: new_answer_vote.answer});
                        $scope.answer.votes -= 1;
                        $scope.user_answer_vote_down = 'active';
                    }
                });
            };
    }]);

    app.factory('AnswerVote', function($resource){
        return $resource('/api/answer_vote/:answer', {}, {
            update: {method: 'PUT'},
        });
    });
    app.factory('QuestionVote', function($resource){
        return $resource('/api/question_vote/:question', {}, {
            update: {method: 'PUT'},
        });
    });

})(angular);