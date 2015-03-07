(function(angular){
    'use strict';

    var module = angular.module('messages.controllers', []);

    // Service to share data across the controllers
    module.factory('messages_list', function() {
        return {
            messages : []
        };
    });

    module.controller('NewMessageController', ['$scope', '$modal', '$window', 'Message', 'Student', 'StudentSearch', 'Class', 'messages_list', '$rootScope',
            function($scope, $modal, $window, Message, Student, StudentSearch, Class, messages_list, $rootScope) {
                $scope.course_id = parseInt($window.course_id, 10);
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
                    $scope.empty_msg_subject_error = false;
                    $scope.empty_msg_body_error = false;

                    $scope.classes = Class.query({course: course_id}, function(classes){
                        classes.checked = [];
                        return classes;
                    });

                    // trick to user modal.all_checked in ng-model html tag
                    $scope.modal = {};
                    $scope.modal.all_checked = true;

                    $scope.send = function () {
                        // TODO validação dos campo: títle e message não podem ser vazios
                        if ($scope.modal.all_checked) {
                            $scope.new_message.users = [];
                            angular.forEach($scope.classes, function(klass) {
                                $scope.new_message.users = $scope.new_message.users.concat(klass.students);
                            });
                        } else if ($scope.classes.checked) {
                            angular.forEach($scope.classes.checked, function(klass) {
                                $scope.new_message.users = $scope.new_message.users.concat(klass);
                            });
                        }
                        if ($scope.new_message.message && $scope.new_message.subject) {
                            $modalInstance.close($scope.new_message);
                            $scope.empty_msg_subject_error = false;
                            $scope.empty_msg_body_error = false;
                        }
                        if (!$scope.new_message.message) {
                            $scope.empty_msg_body_error = true;
                        } else {
                            $scope.empty_msg_body_error = false;
                        }
                        if (!$scope.new_message.subject) {
                            $scope.empty_msg_subject_error = true;
                        } else {
                            $scope.empty_msg_subject_error = false;
                        }
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

    module.controller('MessagesListController', ['$scope', '$modal', '$window', 'Message', 'messages_list',
        function($scope, $modal, $window, Message, messages_list) {
            $scope.course_id = parseInt($window.course_id, 10);
            $scope.course_slug = $window.course_slug;
            messages_list.messages = Message.query({course: $scope.course_id});
            $scope.messages = messages_list.messages;
            $scope.$on('newMessage', function() {
                $scope.messages = messages_list.messages;
            });
        }
    ]);

    module.controller('MessageController', ['$scope', '$window', 'Message',
        function($scope, $window, Message) {
            $scope.course_id = parseInt($window.course_id, 10);
            $scope.message_id = document.location.href.match(/message\/([0-9]+)/)[1];
            $scope.message = Message.get({messageId: $scope.message_id}, function(message) {
            });
        }
    ]);
})(angular);
