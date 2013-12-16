(function(angular){
    'use strict';
    var app = angular.module('new-course');

    app.factory('FormUpload', ['$http', '$q', function($http, $q){
        return function() {
            var formData = new FormData();

            this.addField = function(name, value) {
                formData.append(name, value);
            };

            this.sendTo = function(url) {
                var deferred = $q.defer();

                formData.append('csrfmiddlewaretoken',
                                /csrftoken=(\w+)/.extract(document.cookie, 1));

                var oReq = new XMLHttpRequest();

                oReq.onreadystatechange = function(){
                    if(this.readyState !== 4) return;

                    var response = {};
                    response.data = angular.fromJson(this.responseText || '{}');
                    response.status = this.status;
                    console.log(this);

                    if( this.status === 200  ) {
                        deferred.resolve(response);
                    } else {
                        deferred.reject(response);
                    }
                };

                oReq.open('POST', url, true);
                oReq.send(formData);

                return deferred.promise;
            };
        };
    }]);

    app.factory('getRestOptions', ['$http', function($http){
        return function(url){
            return $http({
                method:'POST',
                url: url,
                data:'_method=OPTIONS',
                headers:{'Content-Type':'application/x-www-form-urlencoded'}
            });
        };
    }]);

    app.factory('Course', ['$resource', '$http', 'getRestOptions', function($resource, $http, getRestOptions) {
        var url_template = '/api/course/:id';
        var Course = $resource(url_template, {'id':'@id'});

        Course.prototype.hasVideo = function(){
            return this.intro_video && this.intro_video.youtube_id &&
                   this.intro_video.youtube_id.length > 0;
        };

        Course.prototype.getUrl = function() {
            var that = this;
            return url_template.replace(/\/:(\w+)/g, function(mark, field){
                var part = '';
                if ( that[field] ) {
                    part = '/' + that[field];
                }
                return part;
            });
        };

        getRestOptions(Course.prototype.getUrl()).success(function(data) {
            Course.fields = angular.copy(data.actions.POST);
        });

        return Course;
    }]);

    app.factory('VideoData', ['$document', '$q', function($document, $q){
        var funcName = 'getYoutubeData'+Math.random().toString(16).substring(2);

        var VideoData = function() {
            this.load = function(vid) {
                this.deferred = $q.defer();

                this.src = 'http://gdata.youtube.com/feeds/api/videos/'+
                            vid + '?alt=json&callback=' + funcName;

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