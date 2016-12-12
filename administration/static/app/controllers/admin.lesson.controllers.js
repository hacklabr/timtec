(function(angular){

    var app = angular.module('admin.lesson.controllers', ['ngSanitize']);

    app.controller('EditLessonController', [
        '$scope',
        'Course',
        'CourseProfessor',
        'Lesson',
        'VideoData',
        'youtubePlayerApi',
        'MarkdownDirective',
        'waitingScreen',
        'Forum',
        function($scope, Course, CourseProfessor, Lesson, VideoData, youtubePlayerApi,
                 MarkdownDirective, waitingScreen, Forum) {
            $scope.errors = {};
            var httpErrors = {
                '400': 'Os campos não foram preenchidos corretamente.',
                '403': 'Você não tem permissão para ver conteúdo nesta página.',
                '404': 'Este curso não existe!'
            };

            // load youtube
            $scope.playerReady = false;
            youtubePlayerApi.loadPlayer().then(function(p){
                $scope.playerReady = true;
            });

            // show the waiting screen
            waitingScreen.show();

            $scope.play = function(youtube_id) {
                youtubePlayerApi.loadPlayer().then(function(player){
                    if(player.getVideoData().video_id === youtube_id) return;
                    player.cueVideoById(youtube_id);
                });
            };

//            $scope.course = new Course();
            $scope.courseProfessors = [];

            var match = document.location.href.match(/courses\/(\d+)\/lessons\/(new|\d+)/);
            if( match ) {

                $scope.course_id = match[1]
                $scope.course = Course.get({id: $scope.course_id});

                $scope.isNewLesson = ('new' === match[2]);
                if (!$scope.isNewLesson) {
                    $scope.lesson_id = match[2];
                }

                Lesson.query({course__id: $scope.course_id}).$promise
                    .then(function(lessons){
                        $scope.lessons = lessons;
                        lessons.forEach(function(lesson){
                            if(lesson.id === parseInt($scope.lesson_id, 10)) {
                                $scope.setLesson(lesson);
                            }
                        });
                        if($scope.isNewLesson) {
                            $scope.lesson = new Lesson();
                            $scope.lesson.course = parseInt($scope.course_id, 10);
                            $scope.lesson.position = $scope.lessons.length;
                            $scope.addUnit();
                            $scope.lessons.push($scope.lesson);
                        }
                        waitingScreen.hide();
                    })['catch'](function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                        waitingScreen.hide();
                    }
                );
            }

            $scope.activityTypes = [
                {'name': 'simplechoice', 'label': 'Escolha simples'},
                {'name': 'multiplechoice', 'label': 'Múltipla escolha'},
                {'name': 'trueorfalse', 'label': 'Verdadeiro ou falso'},
                {'name': 'relationship', 'label': 'Relacionar sentenças'},
                {'name': 'html5', 'label': 'HTML5'},
                {'name': 'markdown', 'label': 'Texto simples'},
                {'name': 'image', 'label': 'Imagem'},
                {'name': 'reading', 'label': 'Atividade de leitura'},
                {'name': 'discussion', 'label': 'Atividade com discussão'},
            ];

            /*  Methods */
            $scope.setLesson = function(l) {
                $scope.lesson = l;
                document.title = 'Aula: {0}'.format(l.name);

                if(l.units.length > 0) {
                    $scope.selectUnit(l.units[0]);
                } else {
                    $scope.addUnit();
                }
            };

            $scope.saveLesson = function() {
                var unitIndex = $scope.lesson.units.indexOf($scope.currentUnit);
                var activityIndex = $scope.currentUnit.activities.indexOf($scope.currentActivity);

                $scope.lesson.saveOrUpdate()
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso.');
                        $scope.selectUnit($scope.lesson.units[unitIndex]);
                        if(activityIndex >= 0) {
                            $scope.currentActivity = $scope.currentUnit.activities[activityIndex];
                        }
                    })['catch'](function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            };

            $scope.publishLesson = function() {
                $scope.lesson.status = 'published';
                $scope.saveLesson();
            };

            $scope.deleteLesson = function() {
                var msg = 'Apagar a aula "'+ $scope.lesson.name + '" e todo seu conteúdo?';

                if(!confirm(msg)) return;

                function backToCourse () {
                    document.location.href = '/admin/courses/{0}'
                                             .format($scope.course.id);
                }

                var index = $scope.lessons.indexOf($scope.lesson);
                if(index >= 0) {
                    $scope.lessons.splice(index, 1);

                    if($scope.lesson.id){
                        msg = 'A aula "{0}" e todo seu conteúdo foram apagados do sistema.'
                              .format($scope.lesson.name);
                        $scope.lesson.$delete().then(function(){
                            $scope.alert.success(msg);
                            backToCourse();
                        });
                    } else {
                        backToCourse();
                    }
                } else {
                    $scope.lesson = new Lesson();
                }
            };

            $scope.selectUnit = function(u) {
                $scope.currentUnit = u;
                if(u.video && u.video.youtube_id){
                    $scope.play(u.video.youtube_id);
                }
                if($scope.currentUnit.activities) {
                    $scope.currentActivity = $scope.currentUnit.activities[0];
                    if($scope.currentActivity && $scope.currentActivity.type === 'discussion'){
                      $scope.initializeDiscussionActivity();
                    }

                }
                $scope.newActivityType = null;

                // MarkdownDirective.resetEditors();
                MarkdownDirective.refreshEditorsPreview();
            };

            $scope.addUnit = function() {
                if(!$scope.lesson.units) {
                    $scope.lesson.units = [];
                }
                $scope.currentUnit = {'activities': []};
                $scope.currentActivity = null;
                $scope.currentUnit.lesson = $scope.lesson.id;
                $scope.lesson.units.push($scope.currentUnit);
                // MarkdownDirective.resetEditors();
                MarkdownDirective.refreshEditorsPreview();
            };

            $scope.removeCurrentUnit = function() {
                if(!$scope.lesson.units) return;
                if(!confirm('Apagar unidade?')) return;
                var index = $scope.lesson.units.indexOf($scope.currentUnit);
                $scope.lesson.units.splice(index,1);

                index = index > 0 ? index - 1 : 0;
                if(index < $scope.lesson.units.length) {
                    $scope.selectUnit($scope.lesson.units[index]);
                }
            };

            $scope.setCurrentUnitVideo = function() {
                var youtube_id = $scope.currentUnit.intended_youtube_id;
                delete $scope.currentUnit.intended_youtube_id;  // prevent this atribute from being sent to the server on object save

                //
                // support pasting both long and short urls from youtube
                // eg. http://youtu.be/8uj7YSqby7s
                //
                var complete_url = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
                var result = complete_url.exec(youtube_id);
                if (result && result[2].length == 11) {
                    youtube_id = result[2];
                }

                if(!$scope.currentUnit.video) {
                    $scope.currentUnit.video = {};
                }
                $scope.currentUnit.video.youtube_id = youtube_id;
                VideoData.load(youtube_id).then(function(data){
                    if (data.items !== undefined && data.items.length > 0) {
                        $scope.currentUnit.video.name = data.items[0].snippet.title;
                        if (!$scope.currentUnit.title)
                            $scope.currentUnit.title = data.items[0].snippet.title;
                    }
                });
                $scope.play(youtube_id);
            };

            $scope.loadActivityTemplateUrl = function() {
                if(!$scope.currentActivity) return;
                return '/static/templates/activities/activity_{0}.html'
                       .format($scope.currentActivity.type);
            };

            $scope.initializeDiscussionActivity = function() {
              $scope.currentActivity.data.start_date = new Date($scope.currentActivity.data.start_date);
              $scope.currentActivity.data.end_date = new Date($scope.currentActivity.data.end_date);
            };

            $scope.$on('$locationChangeStart', function( event ) {
                // TODO
                // Verify if user has saved the discussion activity and if not, delete the created forum.
                // var answer = confirm("Are you sure you want to leave this page?")
                // if (!answer) {
                //     event.preventDefault();
                // }
            });

            $scope.addNewActivity = function(type) {
                if(!$scope.currentUnit) return;
                if(!$scope.currentUnit.activities) $scope.currentUnit.activities = [];

                var expected;
                if (type === 'simplechoice') {
                    expected = 0;
                } else if (type === 'html5') {
                    expected = '';  // shouldn't it be ['']?
                } else {
                        expected = [];
                }

                if(type === 'discussion'){
                    // JSON pattern for the discussion type of activities
                    $scope.currentActivity = {
                        'type': type,
                            'data': {
                                'forum': null,
                                'content': '',
                                'start_date': null,
                                'end_date': null
                            },
                            'expected': ''
                    };

                    // Create a new forum to recieve the students answers
                    var new_forum = new Forum();
                    new_forum.title = 'Fórum de atividades: ' + $scope.lesson.name;
                    new_forum.forum_type = 'activity';
                    new_forum.$save(function(forum) {
                       $scope.currentActivity.data.forum = forum.id;
                    });

                } else {
                  // JSON pattern for other types of activities
                  $scope.currentActivity = {
                      'type': type,
                      'data': {
                          'question': '',
                          'alternatives': [],
                          'column1': [],
                          'column2': []
                      },
                      'expected': expected
                  };
                }

                $scope.currentUnit.activities.push($scope.currentActivity);
                $scope.newActivityType = null;
                MarkdownDirective.refreshEditorsPreview();
            };

            $scope.selectActivity = function(activity) {
                $scope.currentActivity = activity;
                MarkdownDirective.refreshEditorsPreview();
            };

            $scope.removeCurrentActivity = function() {
                if(!$scope.currentUnit) return;
                if(!$scope.currentUnit.activities) return;
                var idx = $scope.currentUnit.activities.indexOf($scope.currentActivity);
                if(idx >= 0) {
                    $scope.currentUnit.activities.splice(idx, 1);
                }
                if(idx > 0) {
                    idx--;
                    $scope.currentActivity = $scope.currentUnit.activities[idx];
                } else if($scope.currentUnit.activities.length > 0) {
                    $scope.currentActivity = $scope.currentUnit.activities[idx];
                } else {
                    $scope.currentActivity = null;
                }
                MarkdownDirective.refreshEditorsPreview();
            };
        }
    ]);

    app.controller('ImageActivityAdminCtrl', [
      '$scope',
      'Upload',
      function ($scope, Upload) {

        // whenever the activity_image.html is reoaded, the next function is called
        $scope.$watch('currentActivity', function() {
            // If there is already an image, show it
            if($scope.currentActivity !== undefined && $scope.currentActivity.image_url)
                $scope.currentActivity.image_show = true;
            else
                $scope.currentActivity.image_show = false;
        });

        $scope.saveImage = function(currentActivity) {
            if(! $scope.image_up) {
                return;
            }
            if ($scope.course.id) {
              // Define the HTTP method
              // If the activity will be created now, must be POST. Otherwise, PUT
              var upload_method;
              var id;
              if(currentActivity.id){
                  upload_method = 'PUT';
                  id = '/'+currentActivity.id;
              }
              else{
                  upload_method = 'POST';
                  id = '';
              }

              Upload.upload({
                url: '/api/activity_image' + id,
                method: upload_method,
                data: {image: $scope.image_up},
              }).then(function(response){
                  $scope.alert.success('A imagem foi atualizada.');
                  currentActivity.id = response.data.id;
                  currentActivity.image_url = response.data.image.match("^[^#]*?:\/\/.*?(\/.*)$")[1];
                  currentActivity.image_show = true;
              });
            }
        };

        $scope.deleteThumb = function() {
            if ($scope.course.id) {
              Upload.upload({
                url: '/api/activity_image/' + $scope.currentActivity.id,
                method: 'PUT',
                data: {image: ''},
              }).then(function(response){

              });
            }
        };

      }
    ]);

})(window.angular);
