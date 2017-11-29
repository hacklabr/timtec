(function(angular) {
  'use strict';

    var app = angular.module('djangular', [])

    app.service('CurrentUser', function () {
      return {
          'username': '{{ user.username|escapejs }}',
          'is_authenticated': 'True' === '{{ user.is_authenticated|escapejs }}',
          {% if user.is_authenticated %}
          'id': '{{ user.id|escapejs }}',
          'name': '{{ user.get_full_name|escapejs }}',
          'picture': '{{ user.get_picture_url|escapejs }}',
          {% endif %}
       }
    });

    app.constant('STATIC_URL', '{{ STATIC_URL }}');
    app.constant('DEBUG', '{{ DEBUG }}');

    app.config(function ($httpProvider, $logProvider, DEBUG, $sceDelegateProvider, STATIC_URL) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $logProvider.debugEnabled(DEBUG);
            $sceDelegateProvider.resourceUrlWhitelist([
                /^https?:\/\/(www\.)?youtube\.com\/.*/,
                'data:text/html, <html style="background: white">',
                'self',
                STATIC_URL + '**'
            ]);
        }
    );

})(angular);
