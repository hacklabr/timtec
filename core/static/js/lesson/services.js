(function(angular){
    'use strict';

    var app = angular.module('lesson.services', []);

    app.factory('Answer',['$resource', '$q',
        function($resource, $q){
            var resourceConfig = {
                'update': {'method': 'PUT'}
            };
            var Answer = $resource('/api/answer/:id', {'id':'@id'}, resourceConfig);

            Answer.prototype.saveOrUpdate = function() {
                return this.id > 0 ? this.$update() : this.$save();
            };

            Answer.getLastGivenAnswer = function(activity_id) {
                var deferred = $q.defer();
                var extractLatest = function (list) {
                    if(list.length > 0) {
                        deferred.resolve(list.pop());
                    } else {
                        deferred.reject();
                    }
                };
                Answer.query({'activity': activity_id}, extractLatest);
                return deferred.promise;
            };

            return Answer;
        }
    ]);

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

    app.factory('resolveActivityTemplate', function(STATIC_URL) {
        return function (typeName) {
            return STATIC_URL + '/templates/activity_'+ typeName + '.html';
        };
    });

})(angular);
