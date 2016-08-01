(function(angular){
    'use strict';

    var app = angular.module('lesson.services', []);

    app.factory('Answer', function($resource){
        return $resource('/api/answer/:activityId', {}, {
            update: {method: 'PUT'}
        });
    });

    app.factory('Progress', ['$resource', '$q', function($resource, $q){
        var Progress = $resource('/api/student_progress/:unit', null,
                                 {'update': { method:'PUT' }});

        Progress.complete = function (unit) {
            var progress = new Progress();
            progress.complete = new Date();
            progress.unit = unit;
            Progress.update({unit: progress.unit}, progress);
            return progress;
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

    app.factory('Student', function($resource) {
        return $resource('/api/course_student/', {}, {});
    });

    app.factory('CourseCertification', function($resource) {
        return $resource('/api/course_certification/', {}, {});
    });

    app.factory('resolveActivityTemplate', ['STATIC_URL', function(STATIC_URL) {
        return function (typeName) {
            return STATIC_URL + 'templates/activity_'+ typeName + '.html';
        };
    }]);

})(angular);
