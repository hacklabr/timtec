
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('notes.controllers', []).
        controller('NoteCtrl', ['$scope', '$window', '$location', 'LessonData', 'Note',
            function ($scope, $window, $location, LessonData, Note) {

                $scope.show_notes = false;

                $scope.save_note = function() {
                    var promisse;
                    $scope.note.text = $scope.note_text;
                    if ($scope.note.id) {
                        promisse = $scope.note.$update({note_id: $scope.note.id});
                    } else {
                        promisse = $scope.note.$save();
                    }
                    promisse.then(function() {
                        $('.notes.message.success').show().delay(2000).fadeOut();
                    }).catch(function() {
                        $('.notes.message.failure').show().delay(2000).fadeOut();
                    });
                };
                function load_note() {
                    LessonData.then(function (lesson) {
                        $scope.currentUnit.$promise.then(function() {
                          var currentUnitId = $scope.currentUnit.id;
                          $scope.currentUnitPos = $scope.findUnitPos($scope.currentUnit);
                          Note.get({content_type: window.unit_content_type_id, object_id: currentUnitId}, function (notes) {
                            if (notes.length > 0){
                              $scope.note = notes[0];
                            } else {
                              $scope.note = new Note();
                              $scope.note.content_type = window.unit_content_type_id;
                              $scope.note.object_id = currentUnitId;
                            }
                            $scope.note_text = $scope.note.text;
                          });
                        });
                    });
                }

                var prevUnitPos = $scope.currentUnitPos;
                $scope.$watch(function() {
                    return $location.path();
                }, function(){
                    if (prevUnitPos != $scope.currentUnitPos) {
                        load_note();
                        prevUnitPos = $scope.currentUnitPos;
                    }
                });

                load_note();
                $scope.$on('$locationChangeStart', function(event, newVal, oldVal) {
                    if ($scope.note && $scope.note.text != $scope.note_text)
                        $scope.save_note();
                });
    }]).
    controller('CourseNotesCtrl', ['$scope', '$window', 'CourseUserNotes', 'Note',
            function ($scope, $window, CourseUserNotes, Note) {
                var course_slug = $window.location.pathname.split('/')[2];
                CourseUserNotes.query({course_slug: course_slug}, function(lessons){

                    function compare(a,b) {
                        if (a.position < b.position)
                           return -1;
                        if (a.position > b.position)
                           return 1;
                        return 0;
                    }
                    lessons.sort(compare);
                    angular.forEach(lessons, function(lesson) {
                        lesson.units_notes.sort(compare);
                    });
                    $scope.lessons = lessons;
                });
                $scope.delele_note = function(course, lesson, unit, note) {
                    if(!confirm('Tem certeza que deseja remover esta anotação?')) return;

                    Note.remove({note_id: note.id}, function (){
                        var index;
                        if (lesson.units_notes.length > 1) {
                            index = lesson.units_notes.indexOf(unit);
                            lesson.units_notes.splice(index, 1);
                        } else {
                            index = $scope.lessons.indexOf(lesson);
                            $scope.lessons.splice(index, 1);
                        }
                    });
                };
    }]).
    controller('UserNotesCtrl', ['$scope', '$window', 'UserNotes', 'Note',
            function ($scope, $window, UserNotes, Note) {
                function compare(a,b) {
                    if (a.position < b.position)
                       return -1;
                    if (a.position > b.position)
                       return 1;
                    return 0;
                }
                UserNotes.query({}, function(courses){
                    angular.forEach(courses, function(course) {
                        course.lessons_notes.sort(compare);
                        angular.forEach(course.lessons_notes, function(lesson) {
                            lesson.units_notes.sort(compare);
                        });
                    });
                    $scope.courses = courses;
                });

                $scope.delele_note = function(course, lesson, unit, note) {
                    if(!confirm('Tem certeza que deseja remover esta anotação?')) return;
                    Note.remove({note_id: note.id}, function (){
                        var index;
                        if (lesson.units_notes.length > 1) {
                            index = lesson.units_notes.indexOf(unit);
                            lesson.units_notes.splice(index, 1);
                        } else {
                            index = course.lessons_notes.indexOf(lesson);
                            course.lessons_notes.splice(index, 1);
                        }
                        course.course_notes_number -= 1;
                    });
                };
    }]);
})(angular);
