(function(angular) {
  'use strict';

    var djangular = angular.module('djangular', [])

    djangular.service('CurrentUser', function () {
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

})(angular);
