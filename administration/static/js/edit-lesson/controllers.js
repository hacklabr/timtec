(function(angular){

    var app = angular.module('edit-lesson');

    app.controller('EditLessonController', ['$scope', 'Course', 'CourseProfessor', 'Lesson', 'youtubePlayerApi',
        function($scope, Course, CourseProfessor, Lesson, youtubePlayerApi){
            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            $scope.course = new Course();
            $scope.lesson = new Lesson();
            $scope.currentUnit = null;
            $scope.courseProfessors = [];

            $scope.setLesson = function(l) {
                $scope.lesson = l;
                if(l.units.length > 0) {
                    $scope.currentUnit = l.units[0];
                }
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/(\d+)\/lessons\/(new|\d+)/);
            if( match ) {
                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        $scope.courseProfessors = CourseProfessor.query({ course: course.id });
                        return $scope.courseProfessors.$promise;
                    });

                Lesson.query({course__id: match[1]}).$promise
                    .then(function(lessons){
                        $scope.lessons = lessons;
                        lessons.forEach(function(lesson){
                            if(lesson.id === parseInt(match[2], 10)) {
                                $scope.setLesson(lesson);
                            }
                        });
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            }
            // ^^ como faz isso de uma formula angular ?

            var player;
            $scope.playerReady = false;
            youtubePlayerApi.loadPlayer().then(function(p){
                player = p;
                $scope.playerReady = true;
            });

            $scope.$watch('currentUnit.video.youtube_id', function(vid, oldVid){
                if(!vid || vid === oldVid) return;
                if(player) player.cueVideoById(vid);
                //VideoData.load(vid).then(function(data){
                //    $scope.course.intro_video.name = data.entry.title.$t;
                //});
            });
        }
    ]);


})(window.angular);
