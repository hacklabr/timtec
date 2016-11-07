(function(angular){

    var app = angular.module('new-course');

    app.controller('CourseEditController',
        ['$scope', '$window', '$modal', '$http', '$q', 'Course',  'CourseAuthor', 'Lesson', '$filter', 'youtubePlayerApi', 'VideoData', 'FormUpload',
        function($scope, $window, $modal, $http , $q, Course,  CourseProfessor, Lesson, $filter, youtubePlayerApi, VideoData, FormUpload) {

            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            $scope.course_id = parseInt($window.course_id, 10);

            $scope.course = new Course();
            $scope.courseProfessors = [];
            $scope.lessons = [];
            window.s = $scope;

            $scope.course.$get({id: $scope.course_id})
                .then(function(course){
                    if(course.intro_video) {
                        youtubePlayerApi.videoId = course.intro_video.youtube_id;
                    }
                    document.title = 'Curso: {0}'.format(course.name);
                    $scope.addThumb = !course.thumbnail_url;
                    $scope.addHomeThumb = !course.home_thumbnail_url;
                })
                .then(function(){
                    $scope.lessons = Lesson.query({'course__id': $scope.course_id});
                    return $scope.lessons.promise;
                })
                .then(function(){
                    $scope.courseProfessors = CourseProfessor.query({
                        course: $scope.course_id
                    });

                    // TODO here comes classes professors

                    return $scope.courseProfessors.promise;
                })['catch'](function(resp){
                    $scope.alert.error(httpErrors[resp.status.toString()]);
                })['finally'](function(){
                    $scope.statusList = Course.fields.status.choices;
                });

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
                    if (data.items.length > 0)
                        $scope.course.intro_video.name = data.items[0].snippet.title;
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

            $scope.export_course = function() {
                $window.open('/admin/course/' + $scope.course_id + '/export/', '_blank', '');
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

                        // remove pop-up that confirm if user go without save changes
                        window.onbeforeunload = function(){};

                    })['catch'](showFieldErrors);
            };

            $scope.publishCourse = function() {
                $scope.course.status = 'published';
                $scope.saveCourse();
            };

            $scope.set_course_as_draft = function() {
                if (confirm('Ao tornar o curso um racunho, ele não será mais visível para os usuários! Tem certeza que deseja tornar este curso um rascunho?')){
                    $scope.course.status = 'draft';
                    $scope.saveCourse();
                }
            };

            $scope.deleteCourse = function() {
                if(!confirm('Tem certeza que deseja remover este curso?')) return;

                $scope.course.$delete()
                    .then(function(){
                        document.location.href = '/admin/courses';
                    });
            };

            $scope.delete_instructor = function(course_author) {

                var confirm_exclude_instructor_msg = 'Tem certeza que deseja remover "{0}" da lista de instrutores deste curso?'.format(course_author.get_name);
                if (window.confirm(confirm_exclude_instructor_msg)){
                    course_author.$delete().then(function(){
                        var index = $scope.courseProfessors.indexOf(course_author);
                        $scope.courseProfessors.splice(index, 1);
                        $scope.alert.success('"{0}" foi removido da lista de instrutores.'.format(course_author.get_name));
                    }, function(){
                        $scope.alert.error('Erro ao remover "{0}" da lista de instrutores.'.format(course_author.get_name));
                    });
                }
            };

            $scope.save_all_instructors = function() {
                var promises_list = [];
                $scope.courseProfessors.forEach(function(course_author) {
                    delete course_author.picture;
                    course_author.$update();
                    promises_list.push(course_author.$promise);
                });
                $q.all([promises_list]).then(function() {
                        $scope.alert.success('Posição dos instrutores salva com sucesso.');
                    }, function() {
                        $scope.alert.error('Não foi possível salvar a posição dos instrutores!');
                    }
                );
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
                        course_professor.position = $scope.courseProfessors.length;

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
                    $scope.course_professor = undefined;
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

            // add pop-up that confirm if user go without save changes
            $scope.$watchCollection('course', function(new_item, old_item) {
                if(old_item.id && new_item != old_item) {
                    window.onbeforeunload = function(){ return true; };
                }
            });
        }
    ]);

})(window.angular);
