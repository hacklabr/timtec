(function(angular){
    'use strict';
    var app = angular.module('courses');

    app.factory('Course', [
        '$resource',
        function ($resource) {
            var Course = $resource('/api/course/:id', {'id':'@id'});

            Course.prototype.isDraft = function() { return this.status === 'draft'; };
            Course.prototype.isListed = function() { return this.status === 'listed'; };
            Course.prototype.isPublished = function() { return this.status === 'published'; };

            return Course;
        }
    ]);

})(window.angular);