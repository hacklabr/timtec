(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', 'Course', '$filter', 'youtubePlayerApi', 'VideoData',
        function($scope, Course, $filter, youtubePlayerApi, VideoData) {
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
                    }, timeout || 3000);
                }
            };
            $scope.alert.reset();

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

    app.directive('file', function(){
        return {
            'restrict': 'E',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {
                var input = document.createElement('input');
                input.type = 'file';
                input.onchange = function(evt) {
                    if(evt.target.files) {
                        ngModel.$setViewValue(evt.target.files[0]);
                    }
                    scope.$apply();
                };

                for( var att in attrs ) {
                    if(! /^ng/.test(att)) {
                        input[att] = element.attr(att);
                    }
                }
                input.className = element.attr('class').replace(/\bng[^ ]+ */g, '').trim();
                element.attr('class', '');

                element.append(input);
            }
        };
    });

    app.directive('localImage', function(){
        return {
            'restrict': 'A',
            'link': function(scope, element, attrs) {
                var img = element[0];
                var reader = new FileReader();

                reader.onload = function(evt) {
                    img.src = evt.target.result;
                };

                if( attrs.ngModel ) {
                    scope.$watch(attrs.ngModel, function(d){
                        if( window.File && d && d.constructor === window.File ) {
                            img.style.display = '';
                            reader.readAsDataURL( d );
                        } else {
                            img.style.display = 'none';
                        }
                    });
                }
            }
        };
    });

})(window.angular);
