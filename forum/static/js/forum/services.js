
(function (angular) {
    'use strict';

    angular.module('forum.services', ['ngRoute', 'ngResource']).
        factory('ForumAnswer', function($resource){
            return $resource('/api/forum_answer/:answerId', {}, {
                update: {method: 'PUT'},
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
        }).
        factory('QuestionNotification', function($resource){
            return $resource('/api/question_notification/', {}, {
                update: {method: 'PUT'},
                get: {
                    method: 'GET',
                    url: '/api/question_notification/:question?user=:user'
                },
                delete: {
                    method: 'DELETE',
                    url: '/api/question_notification/:question?user=:user'
                }
            });
        });
})(angular);
