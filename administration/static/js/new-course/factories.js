(function(angular){
    'use strict';
    var app = angular.module('new-course');


    app.factory('Course', ['$resource', '$http', function($resource, $http) {

        function stripThumbnail(data, headersGetter) {
            console.log(this, arguments);
            data.thumbnail = null;
            return angular.toJson(data);
        }

        var Course = $resource('/api/course/:id', {'id':'@id'}, {
            'save': {
                'method': 'POST',
                'transformRequest': stripThumbnail
            }
        });

        $http({
            method:'POST',
            url:'/api/course',
            data:'_method=OPTIONS',
            headers:{'Content-Type':'application/x-www-form-urlencoded'}
        }).success(function(data) {
            Course.fields = angular.copy(data.actions.POST);
        });

        Course.prototype.hasVideo = function(){
            return this.intro_video && this.intro_video.youtube_id &&
                   this.intro_video.youtube_id.length > 0;
        };


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