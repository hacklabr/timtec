(function(angular){
    'use strict';

    var module = angular.module('messages.controllers', []);

    // Service to share data across the controllers
    module.factory('messages_list', function() {
        return {
            messages : []
        };
    });

    module.controller('NewMessageController', ['$scope', '$modal', 'Message', 'Student', 'StudentSearch', 'Class', 'messages_list', '$rootScope',
            function($scope, $modal,  Message, Student, StudentSearch, Class, messages_list, $rootScope) {
                $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
                $scope.messages = messages_list.messages;
                $scope.new_message = function () {
                    var modalInstance = $modal.open({
                        templateUrl: 'newMessageModal.html',
                        controller: ['$scope', '$modalInstance', 'course_id', SendMessageModalInstanceCtrl],
                        resolve: {
                            course_id: function () {
                                return $scope.course_id;
                            }
                        }
                    });
                    modalInstance.result.then(function (new_message) {
                        new_message.$save({}, function(new_message){
                            messages_list.messages.unshift(new_message);
                            $rootScope.$broadcast('newMessage');
                        });

                    });
                };
                var SendMessageModalInstanceCtrl = function ($scope, $modalInstance, course_id) {

                    $scope.new_message = new Message();
                    $scope.new_message.course = course_id;
                    $scope.new_message.users = [];
                    $scope.recipient_list = [];

                    $scope.students = Student.query({course: $scope.course_id}, function(students) {
                        // Student service refer to CourseStudent django model.
                        $scope.all_users = [];
                        angular.forEach(students, function(user_ref) {
                            $scope.all_users.push(user_ref.user);
                        });
                    });

                    $scope.classes = Class.query({course: $scope.course_id}, function(classes){
                        classes.checked = [];
                        return classes;
                    });

                    // trick to user modal.all_checked in ng-model html tag
                    $scope.modal = {};
                    $scope.modal.all_checked = true;

                    $scope.send = function () {
                        // TODO validação dos campo: títle e message não podem ser vazios
                        if ($scope.modal.all_checked) {
                            $scope.new_message.users = $scope.all_users.map(function(item) { return item.id; });
                        } else if ($scope.classes.checked) {
                            angular.forEach($scope.classes.checked, function(klass) {
                                $scope.new_message.users = $scope.new_message.users.concat(klass);
                            });
                        }
                        $modalInstance.close($scope.new_message);
                    };

                    $scope.cancel = function () {
                        $modalInstance.dismiss();
                    };
                    $scope.getUsers = function(val) {
                        return new StudentSearch(val, course_id);
                    };

                    $scope.on_select_student = function(model) {
                        $scope.new_message.users.unshift(model.id);
                        $scope.recipient_list.unshift(model);
                        $scope.asyncSelected = '';
                    };

                    $scope.remove_student = function(index) {
                        $scope.new_message.users.splice(index, 1);
                        $scope.recipient_list.splice(index, 1);
                };

                };
            }
        ]);

    module.controller('MessagesListController', ['$scope', '$modal', 'Message', 'messages_list',
        function($scope, $modal,  Message, messages_list) {
            $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
            messages_list.messages = Message.query({course: $scope.course_id});
            $scope.messages = messages_list.messages;
            $scope.$on('newMessage', function() {
                $scope.messages = messages_list.messages;
            });
        }
    ]);

    module.controller('MessageController', ['$scope', 'Message',
        function($scope, Message) {
            $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
            $scope.message_id = document.location.href.match(/message\/([0-9]+)/)[1];
            $scope.message = Message.get({messageId: $scope.message_id}, function(message) {
                $scope.message.users_rows = [];
                var row = [];
                var index = 0;
                angular.forEach(message.users_details, function(user) {
                    row.push(user);
                    if (index == 5) {
                        message.users_rows.push(row);
                        row = [];
                        index = 0;
                    } else
                        index++;
                });
            });
        }
    ]);
})(angular);
