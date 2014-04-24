(function(angular){
    'use strict';

    var module = angular.module('messages.controllers', []);
    module.controller('NewMessageController', ['$scope', '$modal', 'Message', 'Student',
            function($scope, $modal,  Message, Student) {
                $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];

                $scope.new_message = function () {
                    var modalInstance = $modal.open({
                        templateUrl: 'newMessageModal.html',
                        controller: SendMessageModalInstanceCtrl,
                        resolve: {
                            course_id: function () {
                                return $scope.course_id;
                            }
                        }
                    });
                    modalInstance.result.then(function (new_message) {
                        new_message.$save({}, function(new_message){
                            $scope.messages.unshift(new_message);
                        });

                    });
                };
                var SendMessageModalInstanceCtrl = function ($scope, $modalInstance, course_id) {

                    $scope.students = Student.query({course: $scope.course_id}, function(students) {
                        // Student service refer to CourseStudent django model.
                        $scope.users_rows = [];
                        $scope.all_users = [];
                        var row = [];
                        var index = 0;
                        // TODO This is ugly! Refactor if you can...
                        angular.forEach(students, function(user_ref) {
                            row.push(user_ref.user);
                            $scope.all_users.push(user_ref.user);
                            // each row will have 6 names
                            if (index == 6) {
                                $scope.users_rows.push(row);
                                row = [];
                                index = 0;
                            } else
                                index++;
                        });
                    });

                    $scope.new_message = new Message();
                    $scope.new_message.course = course_id;


                    // trick to user modal.all_checked in ng-model html tag
                    $scope.modal = {};
                    $scope.checkAll = function() {
                        if ($scope.modal.all_checked)
                            $scope.new_message.users = [];
                        else
                            $scope.new_message.users = $scope.all_users.map(function(item) { return item.id; });
                    };

                    $scope.send = function () {
                        $modalInstance.close($scope.new_message);
                    };

                    $scope.cancel = function () {
                        $modalInstance.dismiss();
                    };
                };
            }
        ]);

    module.controller('MessagesListController', ['$scope', '$modal', 'Message', 'User',
        function($scope, $modal,  Message, User) {
            $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
            $scope.messages = Message.query({course: $scope.course_id});
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
