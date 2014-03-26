(function(angular){
    'use strict';

    var app = angular.module('lesson.services', []);

    app.factory('Answer', function($resource){
        return $resource('/api/answer/:activityId', {}, {
            update: {method: 'PUT'}
        });
    });

    app.factory('Progress', ['$resource', '$q', function($resource, $q){
        var Progress = $resource('/api/student_progress/:id');

        Progress.getProgressByUnitId = function(unit) {
            var deferred = $q.defer();

            if(!unit) {
                deferred.reject('Invalid unit');
            } else {
                Progress.query({unit: unit}, function(progress){
                    if(progress.length === 1) {
                        deferred.resolve(progress[0]);
                    } else {
                        deferred.reject('No progress found');
                    }
                });
            }

            return deferred.promise;
        };

        return Progress;
    }]);

    app.factory('Lesson', ['$resource', function($resource){
        return $resource('/api/lessons/:id/');
    }]);

    app.factory('LessonData', ['$rootScope', '$q', '$resource', '$window', 'Lesson', 'Progress',
        function($rootScope, $q, $resource, $window, Lesson, Progress) {

            var deferred = $q.defer();

            Lesson.get({'id': $window.lessonId}, function (lesson) {
                $rootScope.lesson = lesson;
                deferred.resolve(lesson);
            });

            Progress.query({'unit__lesson': $window.lessonId}, function (progress) {
                deferred.promise.then(function (lesson) {
                    for (var i = progress.length - 1; i >= 0; i--) {
                        var p = progress[i];
                        for (var j = lesson.units.length - 1; j >= 0; j--) {
                            if (lesson.units[j].id === p.unit) {
                                lesson.units[j].progress = p;
                            }
                        }
                    }
                });
            });

            return deferred.promise;
        }
    ]);

    app.factory('resolveActivityTemplate', ['STATIC_URL', function(STATIC_URL) {
        return function (typeName) {
            return STATIC_URL + '/templates/activity_'+ typeName + '.html';
        };
    }]);

})(angular);
