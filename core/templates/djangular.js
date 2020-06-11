(function(angular) {
  'use strict';

    var app = angular.module('djangular', [])

    app.service('CurrentUser', function () {
        var user_data = {
            'username': '{{ user.username|escapejs }}',
            'is_authenticated': 'True' === '{{ user.is_authenticated|escapejs }}',
        }
        {% if user.is_authenticated %}
        var groups = JSON.parse('{{ user.get_group_names|escapejs }}');
        user_data = Object.assign(user_data, {
            'id': '{{ user.id|escapejs }}',
            'name': '{{ user.get_full_name|escapejs }}',
            'first_name': '{{ user.first_name|escapejs }}',
            'picture': '{{ user.get_picture_url|escapejs }}',
            'is_superuser': 'True' === '{{ user.is_superuser|escapejs }}',
            'groups': groups.names,
        });
        {% endif %}
        return user_data;
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
