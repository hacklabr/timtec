(function(angular){

    var app = angular.module('edit-lesson');

    app.controller('EditLessonController', ['$scope', 'Course', 'CourseProfessor', 'Lesson', 'VideoData', 'youtubePlayerApi',
        function($scope, Course, CourseProfessor, Lesson, VideoData, youtubePlayerApi){
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
            // end load youtube

            $scope.play = function(youtube_id) {
                youtubePlayerApi.loadPlayer().then(function(player){
                    if(player.getVideoData().video_id === youtube_id) return;
                    player.cueVideoById(youtube_id);
                });
            };

            $scope.course = new Course();
            $scope.lesson = new Lesson();
            $scope.currentUnit = {};
            $scope.courseProfessors = [];

            $scope.activityTypes = [
                {'name': 'simplechoice', 'label': 'Escolha simples'},
                {'name': 'multiplechoice', 'label': 'Múltipla escolha'},
                {'name': 'trueorfalse', 'label': 'Verdadeiro ou falso'},
                {'name': 'relationship', 'label': 'Relacionar sentenças'},
                {'name': 'html5', 'label': 'HTML5'}
            ];

            /*  Methods */
            $scope.setLesson = function(l) {
                $scope.lesson = l;
                if(l.units.length > 0) {
                    $scope.selectUnit(l.units[0]);
                } else {
                    $scope.addUnit();
                }
            };

            $scope.saveLesson = function() {
                $scope.lesson.saveOrUpdate()
                    .then(function(){
                        $scope.alert.success('Alterações salvas com sucesso.');
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            };

            $scope.selectUnit = function(u) {
                $scope.currentUnit = u;
                $scope.play(u.video.youtube_id);
            };

            $scope.addUnit = function() {
                if(!$scope.lesson.units) {
                    $scope.lesson.units = [];
                }
                $scope.currentUnit = {};
                $scope.lesson.units.push($scope.currentUnit);
            };

            $scope.setCurrentUnitVideo = function(youtube_id) {
                if(!$scope.currentUnit.video) {
                    $scope.currentUnit.video = {};
                }
                $scope.currentUnit.video.youtube_id = youtube_id;
                VideoData.load(youtube_id).then(function(data){
                    $scope.currentUnit.video.name = data.entry.title.$t;
                });
                $scope.play(youtube_id);
            };

            $scope.loadActivityTemplateUrl = function() {
                if(!$scope.currentUnit.activity) return;
                return '/static/templates/activities/activity_{0}.html'
                       .format($scope.currentUnit.activity.type);
            };

            $scope.addNewActivity = function() {
                if(!$scope.currentUnit) return;
                var type = $scope.newActivityType;
                $scope.currentUnit.activity = {
                    'type': type,
                    'data': {
                        'question': '',
                        'alternatives': [],
                        'column1': [],
                        'column2': []
                    },
                    'expected': (type==='simplechoice' || type==='html5') ? '' : []
                };
            };
            /*  End Methods */

            // vv como faz isso de uma formula angular ?
            var match = document.location.href.match(/courses\/(\d+)\/lessons\/(new|\d+)/);
            if( match ) {
                $scope.isNewLesson = ('new' === match[2]);

                $scope.course.$get({id: match[1]})
                    .then(function(course){
                        $scope.courseProfessors = CourseProfessor.query({ course: course.id });
                        $scope.lesson.course = course.slug;
                        return $scope.courseProfessors.$promise;
                    });

                Lesson.query({course__id: match[1]}).$promise
                    .then(function(lessons){
                        $scope.lessons = lessons;
                        lessons.forEach(function(lesson){
                            if(lesson.id === parseInt(match[2], 10)) {
                                $scope.setLesson(lesson);
                            }
                        });
                        if($scope.isNewLesson) {
                            $scope.addUnit();
                        }
                    })
                    .catch(function(resp){
                        $scope.alert.error(httpErrors[resp.status.toString()]);
                    });
            }
            // ^^ como faz isso de uma formula angular ?
        }
    ]);


})(window.angular);
