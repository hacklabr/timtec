(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', 'Course', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, Course, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };


            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/([0-9]+)/);
            $scope.course = new Course({'status':'draft','intro_video': {'youtube_id':''}});
            if( match ) {
                $scope.course.$get({id:match[1]})
                    .then(function(course){
                        youtubePlayerApi.videoId = course.intro_video.youtube_id;
                        $scope.addThumb = !course.thumbnail_url;
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            }
            // ^^ como faz isso de uma formula angular ?

            $scope.statusList = {
                'draft': 'Rascunho',
                'listed': 'Listado',
                'published': 'Publicados'
            };

            var player;
            $scope.playerReady = false;
            youtubePlayerApi.$watch('playerId', function(){
                if ($scope.playerReady)
                    return;

                youtubePlayerApi.videoId = $scope.course.intro_video.youtube_id;
                youtubePlayerApi.playerWidth = '100%';
                youtubePlayerApi.playerHeight = '475px';
                youtubePlayerApi.loadPlayer().then(function(p){
                    player = p;
                    $scope.playerReady = true;
                });
            });

            $scope.$watch('course.intro_video.youtube_id', function(vid, oldVid){
                if(!vid || vid === oldVid) return;
                if(player) player.cueVideoById(vid);
                VideoData.load(vid).then(function(data){
                    $scope.course.intro_video.name = data.entry.title.$t;
                });
            });

            $scope.saveCourse = function() {
                if(!$scope.course.hasVideo()){
                    delete $scope.course.intro_video;
                }
                if(!$scope.course.slug){
                    $scope.course.slug = $filter('slugify')($scope.course.name);
                }

                $scope.course.$save()
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso!');
                        $scope.alert.hide(function(){
                            $scope.$apply();
                        });

                        if($scope.thumbfile) {
                            var fu = new FormUpload();
                            fu.addField('name', $scope.course.name);
                            fu.addField('slug', $scope.course.slug);
                            fu.addField('thumbnail', $scope.thumbfile);
                            return fu.sendTo('/api/coursethumbs/' + $scope.course.id);
                        }
                    })
                    .catch(function(response){
                        $scope.errors = response.data;
                        var messages = [];
                        for(var att in response.data) {
                            var message = response.data[att];
                            if(Course.fields && Course.fields[att]) {
                                message = Course.fields[att].label + ': ' + message;
                            }
                            messages.push(message);
                        }
                        $scope.alert.error('Encontramos alguns erros!', messages, true);
                    });
            };
        }
    ]);

})(window.angular);
