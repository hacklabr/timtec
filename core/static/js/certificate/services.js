
(function (angular) {
    'use strict';

    var module = angular.module('certification');

    module.service('ClassIdGetter', ['$window', function($window){
        return {
            'classEditView' : function(){
                var match = document.location.href.match(/class\/(\d+)/);
                return match[1];
            },
            'courseSettings' : function(){
                var match = document.location.href.match(/admin\/course\/(\d+)\/certificatesettings/)
                return match[1];
            },
            'certificateData' : function(){
                var match = document.location.href.match(/certificate\/([a-zA-Z0-9 _-]+)/)
                return match[1];
            },
            'courseSlug' : function(){
                var match = document.location.href.match(/course\/([a-zA-Z0-9 _-]+)\/course_evaluations/)
                return match[1];
            },
            'certificateDataId' : function(){
                var match = document.location.href.match(/paralapraca\/admin\/certificate_settings\/([a-zA-Z0-9 _-]+)/)
                return parseInt(match[1]);
            },
        }
    }]);

    module.service('CourseClassesService', ['$window', 'Class', function($window, Class){
        var classes =  Class.query({course_id : $window.course_id}, function(c){
            return c;
        })
        return {
            getClasses: function(){
                return classes;
            },

            get: function(index){
                return classes[index];
            }
        };
    }]);

})(angular);
