
(function (angular) {
    'use strict';

    angular.module('forum.services', ['ngRoute', 'ngResource']).
        factory('ForumAnswer', function($resource){
            return $resource('/api/forum_answer/', {}, {
            });
        }).
        factory('Question', function($resource){
            return $resource('/api/forum_question/:questionId', {}, {
                update: {method: 'PUT'},
                query: {method: 'GET', isArray: false }
            });
        }).
        factory('AnswerVote', function($resource){
            return $resource('/api/answer_vote/:answer', {}, {
                update: {method: 'PUT'}
            });
        }).
        factory('QuestionVote', function($resource){
            return $resource('/api/question_vote/:question', {}, {
                update: {method: 'PUT'}
            });
        });
})(angular);
