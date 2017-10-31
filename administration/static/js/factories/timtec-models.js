(function(angular){
    'use strict';

    var app = angular.module('timtec-models', ['ngResource']);


    /**
     * returns a function that creates XMLHttpRequest for different browsers
     */
    app.factory('createXMLHTTPObject', function(){
            var XMLHttpFactories = [
                function () {return new XMLHttpRequest();},
                function () {return new window.ActiveXObject('Msxml2.XMLHTTP');},
                function () {return new window.ActiveXObject('Msxml3.XMLHTTP');},
                function () {return new window.ActiveXObject('Microsoft.XMLHTTP');}
            ];

            function createXMLHTTPObject() {
                var xmlhttp = false;
                for (var i=0;i<XMLHttpFactories.length;i++) {
                    try {
                        xmlhttp = XMLHttpFactories[i]();
                    }
                    catch (e) {
                        continue;
                    }
                    break;
                }
                return xmlhttp;
            }
            return createXMLHTTPObject;
        });


    /**
     * Provide an object that wraps a FormData and a XMLHttpRequest
     * to upload files. Returns a promise with request info.
     */
    app.factory('FormUpload', ['createXMLHTTPObject', '$q', function(createXMLHTTPObject, $q){
        return function() {

            var formData = new FormData();

            this.addField = function(name, value) {
                formData.append(name, value);
            };

            this.sendTo = function(url, method) {
                var deferred = $q.defer();

                formData.append('csrfmiddlewaretoken',
                                /csrftoken=(\w+)/.extract(document.cookie, 1));

                var oReq = createXMLHTTPObject();

                oReq.onreadystatechange = function(){
                    if(this.readyState !== 4) return;

                    var response = {};
                    response.data = angular.fromJson(this.responseText || '{}');
                    response.status = this.status;

                    if( this.status === 200  ) {
                        deferred.resolve(response);
                    } else {
                        deferred.reject(response);
                    }
                };

                if(method){
                    oReq.open(method, url, true);
                } else {
                    oReq.open('POST', url, true);
                }
                oReq.setRequestHeader("X-CSRFToken", /csrftoken=(\w+)/.extract(document.cookie, 1));
                oReq.send(formData);

                return deferred.promise;
            };
        };
    }]);


    /**
     *  Provide a Course Professor class. The property Class.fields contains the
     *  list of fields that reflects Course model in Django
     */
    app.factory('CourseProfessor', ['$resource', function($resource) {

        return $resource('/api/course_professor/:id', {'id':'@id'}, {
            'update': {
                'method': 'PUT'
            }
        });
    }]);


    /**
     *  Provide a Course Author class. The property Class.fields contains the
     *  list of fields that reflects Course model in Django
     */
    app.factory('CourseAuthor', ['$resource', function($resource) {

        return $resource('/api/course_author/:id', {'id':'@id'}, {
            'update': {
                'method': 'PUT'
            }
        });
    }]);


    /**
     * Basic model class to Professor
     */
    app.factory('Professor', ['$resource', function($resource) {
        var resourceConfig = {
            'query':  {
                'method':'GET',
                'params':{
                    'groups__name': 'professors',
                    'ordering': 'first_name'
                },
                'isArray': true
            },
            'save': {
                'method': 'PUT'
            }
        };
        var Professor = $resource('/api/user/:id', {'id':'@id'}, resourceConfig);
        Professor.prototype.getName = function() {
            var name = this.name;
            if(!name && (this.first_name || this.last_name)) {
                name = this.first_name + ' ' + this.last_name;
            }
            return name.trim() || this.username;
        };
        return Professor;
    }]);


    /**
     * Lesson model. The Course has many Lessons
     */
    app.factory('Lesson', ['$resource', function($resource){
        var resourceConfig = {
            'update': {'method': 'PUT'}
        };
        var Lesson = $resource('/api/lessons/:id', {'id':'@id'}, resourceConfig);
        Lesson.prototype.countVideos = function() {
            return (this.units || []).reduce(function(c, u){
                return u.video ? c + 1 : c;
            }, 0);
        };
        Lesson.prototype.countActivities = function() {
            return (this.units || []).reduce(function(c, u){
                return u.activities ? c + u.activities.length : c;
            }, 0);
        };
        Lesson.prototype.saveOrUpdate = function() {
            return this.id > 0 ? this.$update() : this.$save();
        };
        return Lesson;
    }]);

    /**
     * SimpleLesson model (doesn't load activities data to save bandwidth)
     * This is a read only endopoint. For editing, see the Lesson factory.
     */
    app.factory('SimpleLesson', ['$resource', function($resource){
        var resourceConfig = {};
        var SimpleLesson = $resource('/api/simple_lessons/:id', {'id':'@id'}, resourceConfig);
        SimpleLesson.prototype.countVideos = function() {
            return (this.units || []).reduce(function(c, u){
                return u.video ? c + 1 : c;
            }, 0);
        };
        SimpleLesson.prototype.countActivities = function() {
            return (this.units || []).reduce(function(c, u){
                return u.activities ? c + u.activities.length : c;
            }, 0);
        };
        SimpleLesson.prototype.saveOrUpdate = function() {
            return this.id > 0 ? this.$update() : this.$save();
        };
        return SimpleLesson;
    }]);

    app.factory('CourseStudent', function($resource){
        return $resource('/api/course_student/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    });

    app.factory('CertificationProcess', function($resource){
        return $resource('/api/certification_process/:certificateId',
            {'certificateId' : '@id'},
            {'update': {'method': 'PUT'} });
    });

    app.factory('CourseCertification', function($resource){
        return $resource('/api/course_certification/:link_hash',
            {'link_hash' : '@id' },
            {'update': {'method': 'PUT'} });
    });

    /**
     * Basic model class to Evaluation
     */
    app.factory('Evaluation', function($resource){
        return $resource('/api/evaluation/:id', {'id' : '@id'}, {
            'update': {'method': 'PUT'}
        });
    });

    app.factory('CertificateTemplate', function($resource){
       return $resource('/api/certificate_template/:course', {}, {
           'update' : {'method' : 'PUT'},
       });
    });

    /**
     * StudentSearch model. Used in typeahead input with ui.bootstrap.typeahead.
     * It uses http instead resource cause it has to be synchronous.
     */
    app.factory('StudentSearch', ['$http', function($http){
        return function(val, course_id) {
            return $http.get('/api/student_search', {
                params: {
                    name: val,
                    course: course_id,
                    sensor: false
                }
            }).then(function (res) {
                var student_found = [];
                angular.forEach(res.data, function (item) {
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
                    student_found.push(item);
                });
                return student_found;
            });
        };
    }]);

    /**
     * UserSearch model. Used in typeahead input with ui.bootstrap.typeahead.
     * It uses http instead resource cause it has to be synchronous.
     */
    app.factory('UserSearch', ['$http', function($http){
        return function(val, course_id) {
            return $http.get('/api/user_search', {
                params: {
                    name: val,
                    sensor: false
                }
            }).then(function (res) {
                var user_found = [];
                angular.forEach(res.data, function (item) {
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
                    user_found.push(item);
                });
                return user_found;
            });
        };
    }]);


    app.factory('Class', function($resource){
        return $resource('/api/course_classes/:id', {'id' : '@id'}, {
            'update': {'method': 'PUT'}
        });
    });


    /**
     * A object that fetch info from Youtube. It expects a video ID and returns
     * a promise that video info will be fetched.
     */
    app.factory('VideoData', ['$document', '$q', 'YOUTUBE_API_KEY', function($document, $q, YOUTUBE_API_KEY){
        var funcName = 'getYoutubeData'+Math.random().toString(16).substring(2);

        var VideoData = function() {
            this.load = function(vid) {
                this.deferred = $q.defer();

                // youtube service
                //https://www.googleapis.com/youtube/v3/videos?part=snippet&id=7lCDEYXw3mM&key=AIzaSyC7Czwy79W_Xd-ANIIZScJ6aW8dMG13wFQ
                this.src = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' +
                            vid +
                            '&key=' + YOUTUBE_API_KEY +
                            '&alt=json&callback=' + funcName;

                var script = $document[0].createElement('script');
                script.type = 'text/javascript';
                script.src = this.src;
                $document[0].body.appendChild(script);

                return this.deferred.promise;
            };
        };
        var vd = new VideoData();

        window[funcName] = function(data) {
            vd.deferred.resolve(data);
            return data;
        };

        return vd;
    }]);
})(window.angular);
