(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', '$window', '$modal', '$http', 'Course',  'CourseProfessor', 'Lesson', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, $window, $modal, $http , Course,  CourseProfessor, Lesson, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };


            $scope.course_id = parseInt($window.course_id, 10);
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
                        $scope.addHomeThumb = !course.home_thumbnail_url;
                    })
                    .then(function(){
                        $scope.lessons = Lesson.query({'course__id': match[1]});
                        return $scope.lessons.promise;
                    })
                    .then(function(){
                        $scope.courseProfessors = CourseProfessor.query({course: match[1], role: 'instructor'});
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

            $scope.saveHomeThumb = function() {
                if(! $scope.home_thumbfile) {
                    return;
                }

                if ($scope.course.id) {
                    var fu = new FormUpload();
                    fu.addField('home_thumbnail', $scope.home_thumbfile);
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

                if ($scope.course.start_date) {
                    $scope.course.start_date = $filter('date')($scope.course.start_date, 'yyyy-MM-dd');
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
                var professor_name = '';
                if (courseProfessor.user) {
                    professor_name = courseProfessor.user_info.name || courseProfessor.user_info.username;
                } else {
                    professor_name = courseProfessor.name;
                }

                var msg = 'Tem certeza que deseja remover "{0}" da lista de professores deste curso?'.format(professor_name);
                if(!window.confirm(msg)) return;

                courseProfessor.$delete().then(function(){
                    var index = $scope.courseProfessors.indexOf(courseProfessor);
                    $scope.courseProfessors.splice(index, 1);
                    $scope.alert.success('"{0}" foi removido da lista.'.format(professor_name));
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

            $scope.open_professor_modal = function(course_professor) {

                $scope.courseProfessors_original = angular.copy($scope.courseProfessors);
                var modalInstance = $modal.open({
                       templateUrl: 'course_professor_modal.html',
                       controller: CourseProfessorModalInstanceCtrl,
                       resolve: {
                           course_professor: function () {
                               return course_professor;
                           }
                       }
                });

                modalInstance.result.then(function (course_professor) {
                    var course_professor_picture_file = course_professor.course_professor_picture_file;
                    var fu = new FormUpload();
                    fu.addField('picture', course_professor_picture_file);

                    if (course_professor.picture !== null)
                        delete course_professor.picture;

                    if (course_professor.id === undefined){
                        course_professor.course = $scope.course_id;
                        course_professor.role = 'instructor';

                        course_professor.$save({}, function (course_professor){

                            if (course_professor_picture_file){
                                // return a new promise that file will be uploaded
                                fu.sendTo('/api/course_professor_picture/' + course_professor.id)
                                    .then(function(response){
                                        course_professor.get_picture_url = '/media/' + response.data.picture;
                                        course_professor.picture = '/media/' + response.data.picture;
                                        //$scope.alert.success('A imagem atualizada.');
                                });
                            }

                            $scope.courseProfessors.push(course_professor);
                            $scope.alert.success('Professor do curso atualizado com sucesso!');
                        }, function (){
                            $scope.alert.error('Não foi possível atualizar o professor do curso!');
                        });
                    } else {
                        course_professor.$update({id: course_professor.id}, function (){
                            if (course_professor_picture_file){
                                // return a new promise that file will be uploaded
                                fu.sendTo('/api/course_professor_picture/' + course_professor.id)
                                    .then(function(response){
                                        course_professor.get_picture_url = '/media/' + response.data.picture;
                                        course_professor.picture = '/media/' + response.data.picture;
                                });
                            }
                            $scope.alert.success('Professor do curso atualizado com sucesso!');
                        }, function (){
                            $scope.alert.error('Não foi possível atualizar o professor do curso!');
                        });
                    }
                },
                function() {
                    $scope.courseProfessors = angular.copy($scope.courseProfessors_original);
                });
            };

            var CourseProfessorModalInstanceCtrl = function($scope, $modalInstance, course_professor) {
                if (course_professor === undefined) {
                    course_professor = new CourseProfessor();
                    $scope.linked_with_user = null;
                }

                $scope.course_professor = course_professor;

                $scope.link_user_on = function () {
                    $scope.linked_with_user = true;
                    if (course_professor.user) {
                        if (!course_professor.name && course_professor.user_info.name) {
                            $scope.name_from_user_profile = true;
                        }

                        if (!course_professor.biography && course_professor.user_info.biography) {
                            $scope.biography_from_user_profile = true;
                        }

                        if (!course_professor.picture && course_professor.user_info.picture) {
                            $scope.picture_from_user_profile = true;
                        }
                    }
                };


                if (course_professor.user_info) {
                    $scope.link_user_on();
                } else if ($scope.course_professor.id) {
                    $scope.linked_with_user = false;
                }


                $scope.remove_user_link = function () {
                    $scope.linked_with_user = false;
                    $scope.name_from_user_profile = false;
                    $scope.biography_from_user_profile = false;
                    $scope.picture_from_user_profile = false;
                    $scope.show_form = true;
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };

                $scope.on_select_professor = function(model) {
                    $scope.course_professor.user = model.id;
                    $scope.course_professor.user_info = model;
                    $scope.link_user_on();
                    $scope.show_form = true;
                };

                $scope.remove_professor = function() {
                    $scope.course_professor.user = null;
                    $scope.course_professor.user_info = null;
                    $scope.name_from_user_profile = false;
                    $scope.biography_from_user_profile = false;
                    $scope.picture_from_user_profile = false;
                };

                $scope.save_course_professors = function() {

                    if ($scope.linked_with_user) {
                        if ($scope.name_from_user_profile) {
                            $scope.course_professor.name = null;
                        }
                        if ($scope.biography_from_user_profile) {
                            $scope.course_professor.biography = null;
                        }
                        if ($scope.picture_from_user_profile) {
                            $scope.course_professor.picture = null;
                            $scope.course_professor.get_picture_url = null;
                        }
                    } else {
                        if ($scope.course_professor.user) {
                            delete $scope.course_professor.user;
                        }
                    }


                    if ($scope.course_professor_picture_file && !$scope.picture_from_user_profile) {
                        $scope.course_professor.course_professor_picture_file = $scope.course_professor_picture_file;
                    }
                    $modalInstance.close($scope.course_professor);
                };

                $scope.getUsers = function(val) {
                    return $http.get('/api/user_search', {
                        params: {
                          name: val,
                          sensor: false
                        }
                    }).then(function(res){
                        var professors_found = [];
                        angular.forEach(res.data, function(item){
                            var formated_name = '';
                            if (item.first_name)
                                formated_name += item.first_name;
                            if (item.last_name)
                                formated_name = formated_name + ' ' + item.last_name;
                            if (formated_name)
                                formated_name = formated_name + ' - ';
                            formated_name += item.username;
                            if (item.email)
                                formated_name = formated_name + ' - ' + item.email;
                            item.formated_name = formated_name;
                            professors_found.push(item);
                        });
                        return professors_found;
                    });
                };
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
