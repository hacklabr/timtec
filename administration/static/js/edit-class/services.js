(function(angular){
	'use strict';
	var app = angular.module('edit_class.services', ['ngResource']);

	app.factory('Contracts', ['$resource', function($resource) {
        return $resource('/paralapraca/api/contract/:id',
			{'id': '@id'});
	}]);

})(window.angular);