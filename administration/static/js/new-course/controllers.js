(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', 'Course',  'CourseProfessor', 'Lesson', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, Course,  CourseProfessor, Lesson, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/([0-9]+)/);
            $scope.course = new Course();
            $scope.courseProfessors = [];
            $scope.lessons = [];
            window.s = $scope;

            if( match ) {
                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        if(course.intro_video) {
                            youtubePlayerApi.videoId = course.intro_video.youtube_id;
                        }
                        document.title = 'Curso: {0}'.format(course.name);
                        $scope.addThumb = !course.thumbnail_url;
                        // course_material and forum urls
                        $scope.course_material_url = 'admin/course/' + course.id  + '/material/';
                        $scope.forum_url = 'admin/course/' + course.id +  '/forum/';
                        $scope.messages_url = 'admin/course/' + course.id   + '/messages/';
                        $scope.reports_url = 'admin/course/' + course.id   + '/stats/';
                    })
                    .then(function(){
                        $scope.lessons = Lesson.query({'course__id': match[1]});
                        return $scope.lessons.promise;
                    })
                    .then(function(){
                        $scope.courseProfessors = CourseProfessor.query({ course: match[1] });
                        return $scope.courseProfessors.promise;
                    })['catch'](function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    })['finally'](function(){
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

            $scope.saveThumb = function() {
                if(! $scope.thumbfile) {
                    return;
                }

                if ($scope.course.id) {
                    var fu = new FormUpload();
                    fu.addField('thumbnail', $scope.thumbfile);
                    // return a new promise that file will be uploaded
                    return fu.sendTo('/api/coursethumbs/' + $scope.course.id)
                        .then(function(){
                            $scope.alert.success('A imagem atualizada.');
                        });
                }
            };

            $scope.saveCourse = function() {
                if(!$scope.course.hasVideo()){
                    delete $scope.course.intro_video;
                }
                if(!$scope.course.slug){
                    $scope.course.slug = $filter('slugify')($scope.course.name);
                }

                $scope.course.save()
                    .then(function(){
                        return $scope.saveThumb();
                    })
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso!');
                    })['catch'](showFieldErrors);
            };

            $scope.publishCourse = function() {
                $scope.course.status = 'published';
                $scope.saveCourse();
            };

            $scope.deleteCourse = function() {
                if(!confirm('Tem certeza que deseja remover este curso?')) return;

                $scope.course.$delete()
                    .then(function(){
                        document.location.href = '/admin/courses';
                    });
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
                        return $scope.course.save().then(function(course){
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
                })['catch'](showFieldErrors);
            };

            $scope.saveLesson = function(lesson) {
                return lesson.saveOrUpdate()
                    .then(function(){
                        $scope.alert.success('Lição atualizada com sucesso');
                    })['catch'](function(){
                        $scope.alert.error('Não foi possível salvar a lição');
                    });
            };

            $scope.deleteLesson = function(lesson) {
                var msg = 'Tem certeza que deseja remover a lição "{0}"'.format(lesson.name);
                if(!window.confirm(msg)) return;

                return lesson.$delete().then(function(){
                    var filter = function(l) { return l.id !== lesson.id; };
                    $scope.lessons = $scope.lessons.filter(filter);
                    $scope.alert.success('"{0}" foi removido.'.format(lesson.name));
                });
            };

            $scope.repositionLessons = function() {
                $scope.lessons.forEach(function(lesson, i){
                    lesson.position = i;
                });
            };

            $scope.repositionInstructors = function() {
                $scope.courseProfessors.forEach(function(p, i){
                    p.position = i;
                });
            };

            $scope.saveAllLessons = function() {
                var i = 0;
                function __saveLessons() {
                    if(i < $scope.lessons.length) {
                        return $scope.lessons[i++]
                                     .saveOrUpdate()
                                     .then(__saveLessons);
                    }
                }

                $scope.alert.warn('Atualizando aulas');

                __saveLessons()
                    .then(function(){
                        $scope.alert.success('As aulas foram atualizadas');
                    })['catch'](function(){
                        $scope.alert.error('Algum problema impediu a atualização das aulas');
                    });
            };

            $scope.saveAllInstructors = function() {
                var i = 0;
                function __saveInstructors() {
                    if(i < $scope.courseProfessors.length) {
                        return $scope.courseProfessors[i++]
                                     .saveOrUpdate()
                                     .then(__saveInstructors);
                    }
                }

                $scope.alert.warn('Atualizando dados dos professores');

                __saveInstructors()
                    .then(function(){
                        $scope.alert.success('Os dados dos professores foram atualizados.');
                    })['catch'](function(){
                        $scope.alert.error('Algum problema impediu a atualização dos dados dos professores.');
                    });
            };
        }
    ]);

})(window.angular);
