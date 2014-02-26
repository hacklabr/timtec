(function(angular){

    angular.module('messages.controllers', []).
        controller('NewMessageController', ['$scope', '$modal', 'Message', 'Student',
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
                    modalInstance.result.then(function (question) {
                        question.$update({questionId: question.id}, function(question){
                            question.hidden_to_user = false;
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
                    // trick to user modal.all_checked in ng-model html tag
                    $scope.modal = {};
                    $scope.checkAll = function() {
                        if ($scope.modal.all_checked)
                            $scope.new_message.users = [];
                        else
                            $scope.new_message.users = $scope.all_users.map(function(item) { return item.id; }); 
                    };

                    $scope.send = function () {
                        // $scope.question.hidden = true;
                        // $scope.question.hidden_by = $window.user_id;
                        // $scope.question.hidden_justification = $scope.question.hidden_justification;
                        // $modalInstance.close($scope.question);
                        $modalInstance.close();
                    };

                    $scope.cancel = function () {
                        $modalInstance.dismiss();
                    };
                };
            }
        ]).
        controller('MessagesListController', ['$scope', '$modal', 'Message', 'User',
            function($scope, $modal,  Message, User) {
                $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
                $scope.messages = Message.query({course: $scope.course_id});
            }
        ]).
        controller('MessageController', ['$scope', 'Message', 'User',
            function($scope,  Message, User) {
                $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
                $scope.message_id = document.location.href.match(/message\/([0-9]+)/)[1];
                $scope.message = Message.get({messageId: $scope.message_id}, function(message) {
                    message.users_rows = [];
                    var row = [];
                    var index = 0;
                    angular.forEach(message.users, function(user) {
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
