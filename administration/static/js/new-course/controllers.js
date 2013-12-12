(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', 'Course', '$filter', 'youtubePlayerApi', 'VideoData',
        function($scope, Course, $filter, youtubePlayerApi, VideoData) {
            $scope.errors = {};
            $scope.alert = {
                hidden : true,
                reset: function(){
                    this.title = '';
                    this.type = '';
                    this.messages = [];
                    this.showControls= true;
                }
            };
            $scope.alert.reset();

            window.Course = Course

            $scope.course = new Course({'status':'draft','intro_video': {'youtube_id':''}});
            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/([0-9]+)/);
            if( match ) {
                $scope.course.$get({id:match[1]})
                    .catch(function(resp){
                        $scope.alert.reset();
                        $scope.alert.showControls = false;
                        $scope.alert.type = 'danger';

                        if( resp.status === 404) {
                            $scope.alert.title = 'Curso com não existe!';
                        } else if( resp.status === 403) {
                            $scope.alert.title = 'Você não tem permissão para editar cursos!';
                        } else {
                            $scope.alert.title = 'Ocorreu um erro não esperado.';
                        }
                        $scope.alert.hidden = false;
                    });
                delete match;
            }
            // ^^ como faz isso de uma formula angular ?

            $scope.statusList = {
                'draft': 'Rascunho',
                'listed': 'Listado',
                'published': 'Publicados'
            };

            var player;
            youtubePlayerApi.$watch('playerId', function(){
                youtubePlayerApi.videoId = $scope.course.intro_video.youtube_id;
                youtubePlayerApi.playerWidth = '100%';
                youtubePlayerApi.playerHeight = '475px';
                youtubePlayerApi.loadPlayer().then(function(p){
                    player = p;
                });
            });

            $scope.$watch('course.intro_video.youtube_id', function(vid){
                if(!vid) return;
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
                        $scope.alert.reset();
                        $scope.alert.showControls = false;
                        $scope.alert.type = 'success';
                        $scope.alert.title = 'Alterações salvas com sucesso!';

                        $scope.alert.hidden = false;
                        setTimeout(function(){
                            $scope.alert.hidden = true;
                            $scope.$apply();
                        }, 3000);
                    })
                    .catch(function(response){
                        $scope.errors = response.data;
                        $scope.alert.reset();
                        $scope.alert.type = 'danger';
                        $scope.alert.title = 'Encontramos alguns erros! Verifique os campos abaixo:';
                        for(var att in response.data) {
                            var label = (Course.fields[att]||{}).label ? Course.fields[att].label : att;
                            $scope.alert.messages.push(
                                label + ': ' + response.data[att]
                            );
                        }
                        $scope.alert.hidden = false;
                    }
                );
            };
        }
    ]);

})(window.angular);