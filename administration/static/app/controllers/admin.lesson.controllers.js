(function(angular){

    var app = angular.module('admin.lesson.controllers', ['ngSanitize']);

    app.controller('EditLessonController', [
        '$scope',
        '$location',
        'Course',
        'CourseProfessor',
        'SimpleLesson',
        'Lesson',
        'Unit',
        'VideoData',
        'youtubePlayerApi',
        'MarkdownDirective',
        'waitingScreen',
        'Forum',
        'ForumFile',
        'ContentFile',
        'uiTinymceConfig',
        function($scope, $location, Course, CourseProfessor, Lesson, LessonUpdate, Unit, VideoData, youtubePlayerApi,
                 MarkdownDirective, waitingScreen, Forum, ForumFile, ContentFile, uiTinymceConfig) {
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
                    try {
                        if(player.getVideoData().video_id === youtube_id) return;
                    }
                    catch(err) {
                        // There has been an error trying to get video data from the player API (provided by Youtube)
                        // Pass this error silently
                    }
                    // Enforce now which video must be played
                    player.cueVideoById(youtube_id);
                });
            };

            // Set tinyMCE editor configurations
            uiTinymceConfig.automatic_uploads = true;
            uiTinymceConfig.images_upload_handler = ContentFile.upload;


            // $scope.course = new Course();
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
                    }).catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]  || 'Erro ' + resp.status);
                        waitingScreen.hide();
                    }
                );
            }

            $scope.activityTypes = [
                // {'name': 'simplechoice', 'label': 'Escolha simples'},
                {'name': 'multiplechoice', 'label': 'Múltipla escolha'},
                // {'name': 'trueorfalse', 'label': 'Verdadeiro ou falso'},
                // {'name': 'relationship', 'label': 'Relacionar sentenças'},
                // {'name': 'html5', 'label': 'HTML5'},
                // {'name': 'markdown', 'label': 'Texto simples'},
                {'name': 'image', 'label': 'Imagem'},
                {'name': 'reading', 'label': 'Atividade de leitura'},
                {'name': 'discussion', 'label': 'Atividade com discussão'},
                {'name': 'slidesreveal', 'label': 'Atividade de slides com reveal.js'},
            ];

            /*  Methods */
            $scope.setLesson = function(l) {
                $scope.lesson = l;
                document.title = 'Aula: {0}'.format(l.name);

                if(l.units.length > 0) {
                    var u = $location.search().unit ?
                        l.units[$location.search().unit] : undefined;

                    u = u ? l.units[$location.search().unit] : l.units[0];
                    $scope.selectUnit(u)
                } else {
                    $scope.addUnit();
                }
            };

            $scope.saveLesson = function() {
                var unitIndex = $scope.lesson.units.indexOf($scope.currentUnit);
                var activityIndex = $scope.currentUnit.activities.indexOf($scope.currentActivity);

                lesson = new LessonUpdate($scope.lesson);

                lesson.saveOrUpdate()
                    .then(function(lesson){
                        $scope.lesson = lesson;
                        $scope.alert.success('Alterações salvas com sucesso.');
                        $scope.selectUnit($scope.lesson.units[unitIndex]);
                        if(activityIndex >= 0) {
                            $scope.currentActivity = $scope.currentUnit.activities[activityIndex];
                        }
                        window.location.replace('/admin/courses/' + lesson.course + '/lessons/' + lesson.id);
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
                if (u && u.id) {
                    Unit.get({id : u.id}, function(data){
                        setupUnit(data)
                    });
                } else {
                    setupUnit(u);
                }
                function setupUnit(u){
                    $scope.currentUnit = u;

                    for(i = 0; i < $scope.lesson.units.length; i++){
                        if($scope.lesson.units[i].id == u.id){
                            $scope.lesson.units[i] = u;
                        }
                    }
                    if(u.video && u.video.youtube_id){
                        $scope.play(u.video.youtube_id);
                    }
                    if($scope.currentUnit.activities) {
                        $scope.currentActivity = $scope.currentUnit.activities[0];
                        if($scope.currentActivity && $scope.currentActivity.type === 'discussion'){
                          $scope.initializeDiscussionActivity();
                        }
                    }
                    $location.search('unit', u.position || 0);
                    $scope.newActivityType = null;

                    // MarkdownDirective.resetEditors();
                    MarkdownDirective.refreshEditorsPreview();
                }
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
              Forum.get({id: $scope.currentActivity.data.forum}, function(forum){
                $scope.currForum = forum;
              })
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
                       $scope.currForum = forum;
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
            $scope.uploadForumFiles = function (file, forum) {
                if (file) {
                    ForumFile.upload(file, $scope.currForum.id).then(function (response) {
                        var forum_file = new ForumFile(response.data);
                        if (forum.files === undefined)
                            forum.files = [];
                        forum.files.push(forum_file);
                        return response;
                    }, function (response) {
                        if (response.status > 0) {
                            $scope.alert.error(response.status + ': ' + response.data);
                        }
                    }, function (evt) {
                        forum.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                    });
                }
            };
        }
    ]);

    app.controller('ImageActivityAdminCtrl', [
      '$scope',
      'Upload',
      function ($scope, Upload) {

        // whenever the activity_image.html is reloaded, the next function is called
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

    app.controller('SlidesRevealAdminCtrl', [
      '$scope',
      '$sce',
      'Upload',
      function ($scope, $sce, Upload) {

        // whenever the activity_slidesreveal.html is reloaded, the next function is called
        $scope.$watch('currentActivity', function() {
            // If there is already a slides html, show it
            if($scope.currentActivity !== undefined && $scope.currentActivity.data.content){
                $scope.currentActivity.html_show = true;
            }
            else
                $scope.currentActivity.html_show = false;
        });

        // The html file recieved through the from must be open, read, and its contents will be stored in a json
        $scope.saveSlides = function(currentActivity){
            Upload.dataUrl($scope.html_file, true).then(function(data_url) {
                var blob = Upload.dataUrltoBlob(data_url, "name");
                var reader = new FileReader();
                reader.addEventListener("loadend", function() {
                    currentActivity.data = {
                        'content': reader.result
                    };
                    currentActivity.html_show = true;
                });
                reader.readAsText(blob);
            });
        };

      }]);

})(window.angular);
