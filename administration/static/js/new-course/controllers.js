(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', 'Course',  'CourseProfessor', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, Course,  CourseProfessor, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/([0-9]+)/);
            $scope.course = new Course();
            $scope.courseProfessors = [];

            if( match ) {
                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        if(course.intro_video) {
                            youtubePlayerApi.videoId = course.intro_video.youtube_id;
                        }
                        $scope.addThumb = !course.thumbnail_url;
                        $scope.courseProfessors = CourseProfessor.query({ course: match[1] });
                        return $scope.courseProfessors.promise;
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    })
                    .finally(function(){
                        $scope.statusList = Course.fields.status.choices;
                    });
            }
            // ^^ como faz isso de uma formula angular ?

            var player;
            $scope.playerReady = false;
            youtubePlayerApi.loadPlayer().then(function(p){
                player = p;
                $scope.playerReady = true;
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
                        if($scope.thumbfile) {
                            var fu = new FormUpload();
                            fu.addField('thumbnail', $scope.thumbfile);
                            // return a new promise that file will be uploaded
                            return fu.sendTo('/api/coursethumbs/' + $scope.course.id);
                        }
                    })
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

            $scope.deleteProfessor = function(courseProfessor) {
                var msg = 'Tem certeza que deseja remover '+ courseProfessor.name +
                          'da lista de professores deste curso?';
                if(!window.confirm(msg)) return;

                courseProfessor.$delete().then(function(){
                    var filter = function(p) { return p.user !== courseProfessor.user; };
                    $scope.courseProfessors = $scope.courseProfessors.filter(filter);
                    $scope.alert.success('O professor foi removido.');
                });
            };

            $scope.addProfessor = function(professor) {
                if(!professor) return;
                var copy = angular.copy(professor);
                var mod = copy.first_name.charAt(copy.first_name.length-1) === 'o' ? ['O', '', 'o'] : ['A', 'a', 'a'];

                var reduce = function(a,b){ return a || b.user === copy.id; };

                if($scope.courseProfessors.reduce(reduce, false)) {
                    $scope.alert.error(mod[0]+' professor' + mod[1] + ' ' +
                                       copy.name + ' já foi selecionad' + mod[2] + '.');
                    return;
                }

                var professorToAdd = new CourseProfessor({
                    'user': copy.id,
                    'course': $scope.course.id,
                    'biography': copy.biography,
                    'role': 'instructor',
                    'user_info': copy
                });

                $scope.courseProfessors.push(professorToAdd);
                professorToAdd.$save().then(function(){
                    $scope.alert.success(mod[0] +' professor' + mod[1] + ' ' +
                                         copy.name + ' foi adicionad' + mod[2] + '.');
                });
            };
        }
    ]);

})(window.angular);
