
(function (angular) {
    'use strict';
    /* Controllers */
    angular.module('notes.controllers', []).
        controller('NoteCtrl', ['$scope', '$window', '$location', 'LessonData', 'Note',
            function ($scope, $window, $location, LessonData, Note) {
                $scope.save_note = function() {
                    $scope.note.text = $scope.note_text;
                    if ($scope.note.id) {
                        $scope.note.$update({note_id: $scope.note.id});
                    } else {
                        $scope.note.$save();
                    }
                };
                function load_note() {
                    LessonData.then(function (lesson) {
                        var currentUnit = lesson.units[$scope.currentUnitPos - 1];
                        var currentUnitId = currentUnit.id;
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
    controller('CourseNotesCtrl', ['$scope', '$window', '$location', 'UserNotes', 'Note',
            function ($scope, $window, $location, UserNotes, Note) {
                UserNotes.query({}, function(notes){
                    var lessons = [];
                    var lessons_ids = [];
                    function compare(a,b) {
                        if (a.content_object.position < b.content_object.position)
                           return -1;
                        if (a.content_object.position > b.content_object.position)
                           return 1;
                        return 0;
                    }
                    var lesson = [];
                    var index = -1;
                    angular.forEach(notes, function(note) {
                        lesson = note.lesson;
                        delete note.lesson;
                        index = lessons_ids.indexOf(lesson.id);
                        if (index === -1) {
                            index = lessons.length;
                            lesson.notes = [];
                            lessons.push(lesson);
                            lessons_ids.push(lesson.id);
                        }
                        lessons[index].notes.push(note);
                    });
                    angular.forEach(lessons, function(lesson) {
                        lesson.notes.sort(compare);
                    });
                    $scope.lessons = lessons;
                });
    }]);
})(angular);
