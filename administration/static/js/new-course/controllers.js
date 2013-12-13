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
                    this.showControls=false;
                },
                popup: function(title, messages, showControls){
                    this.reset();
                    this.title = title;
                    this.messages = messages;
                    this.showControls = showControls;
                    this.hidden = false;
                },
                success: function(){
                    this.popup.apply(this, arguments);
                    this.type = 'success';
                },
                error: function(){
                    this.popup.apply(this, arguments);
                    this.type = 'danger';
                },
                hide: function(callback, timeout) {
                    var that = this;
                    setTimeout(function(){
                        that.hidden = true;
                        callback.call();
                    }, timeout || 2000);
                }
            };
            $scope.alert.reset();

            $scope.course = new Course({'status':'draft','intro_video': {'youtube_id':''}});
            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/([0-9]+)/);
            if( match ) {
                $scope.course.$get({id:match[1]})
                    .catch(function(resp){
                        if( resp.status === 404) {
                            $scope.alert.error('Curso com não existe!');
                        } else if( resp.status === 403) {
                            $scope.alert.error('Você não tem permissão para editar cursos!');
                        } else {
                            $scope.alert.error('Ocorreu um erro não esperado.');
                        }
                    });
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
                        $scope.alert.success('Suas alterações salvas!');
                        $scope.alert.hide(function(){
                            $scope.$apply();
                        });
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
