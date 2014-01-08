(function(angular){

    var app = angular.module('edit-lesson');

    app.controller('EditLessonController', ['$scope', 'Course', 'Lesson', 'youtubePlayerApi',
        function($scope, Course, Lesson, youtubePlayerApi){
            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/(\d+)\/lessons\/(new|\d+)/);
            $scope.course = new Course();
            $scope.lesson = new Lesson();
            $scope.currentUnit = null;

            if( match ) {
                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        return Lesson.query({course__slug: course.slug}).$promise;
                    })
                    .then(function(lessons){
                        $scope.lessons = lessons;
                        lessons.forEach(function(lesson){
                            if(lesson.id === parseInt(match[2], 10)) {
                                $scope.lesson = lesson;
                                if(lesson.units.length > 0) {
                                    $scope.currentUnit = lesson.units[0];
                                    youtubePlayerApi.videoId = $scope.currentUnit.video.youtube_id;
                                }
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
