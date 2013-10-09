'use strict';

/* Services */


angular.module('forum.services', ['ngRoute', 'ngResource']).
    factory('Answer', function($resource){
        return $resource('/api/forum_answer/', {}, {
        });
    });
