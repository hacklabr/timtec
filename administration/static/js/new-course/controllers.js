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

            function showFieldErrors(response) {
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
            }

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
                    .catch(showFieldErrors);
            };

            $scope.deleteProfessor = function(courseProfessor) {
                var professor_name = courseProfessor.user_info.name;
                var msg = 'Tem certeza que deseja remover "{0}" da lista de professores deste curso?'.format(professor_name);
                if(!window.confirm(msg)) return;

                courseProfessor.$delete().then(function(){
                    var filter = function(p) { return p.user !== courseProfessor.user; };
                    $scope.courseProfessors = $scope.courseProfessors.filter(filter);
                    $scope.alert.success('"{0}" foi removido da list.'.format(professor_name));
                });
            };

            $scope.saveProfessor = function(courseProfessor) {
                function __saveProfessor(){
                    if (!$scope.course.id) {
                        return $scope.course.$save().then(function(course){
                            courseProfessor.course = course.id;
                            return courseProfessor.saveOrUpdate();
                        });
                    }
                    return courseProfessor.saveOrUpdate();
                }
                return __saveProfessor().then(function(){
                    $scope.alert.success('{0} foi atualizado'.format(courseProfessor.user_info.name));
                });
            };

            $scope.pi = function(p) {
                return function(){ window.alert(p); };
            };

            $scope.addProfessor = function(professor) {
                if(!professor) return;
                var copy = angular.copy(professor);

                var reduce = function(a,b){ return a || b.user === copy.id; };

                if($scope.courseProfessors.reduce(reduce, false)) {
                    $scope.alert.error('"{0}" já está na lista de professores deste curso.'.format(copy.name));
                    return;
                }

                var professorToAdd = new CourseProfessor({
                    'user': copy.id,
                    'course': $scope.course.id,
                    'biography': copy.biography,
                    'role': 'instructor',
                    'user_info': copy
                });

                $scope.saveProfessor(professorToAdd).then(function(){
                    $scope.alert.success('"{0}" foi adicionado a lista de professores.'.format(copy.name));
                    $scope.courseProfessors.push(professorToAdd);
                }).catch(showFieldErrors);
            };
        }
    ]);

})(window.angular);
