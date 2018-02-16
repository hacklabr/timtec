(function(angular){
    'use strict';

    var app = angular.module('admin.lesson.services', []);

    app.factory('Unit', ['$resource', function($resource){
        return $resource('/api/unit/:id/');
    }]);

    /**
     * SimpleLesson model (doesn't load activities data to save bandwidth)
     * This is a read only endopoint
     */
    app.factory('SimpleLesson', ['$resource', function($resource){
        var resourceConfig = {};
        var SimpleLesson = $resource('/api/simple_lessons/:id', {'id':'@id'}, resourceConfig);
        return SimpleLesson;
    }]);

})(angular);
