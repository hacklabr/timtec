(function(angular){

    angular.module('messages.controllers', []).
        controller('NewMessageController', ['$scope', '$modal', 'Message', 'User',
            function($scope, $modal,  Message, User) {
                $scope.course_id = document.location.href.match(/course\/([0-9]+)/)[1];
                // $scope.messages = Message.query({course: $scope.course_id});

                var SendMessageModalInstanceCtrl = function ($scope, $modalInstance) {
                    // $scope.question = question;

                    $scope.send = function () {
                        // $scope.question.hidden = true;
                        // $scope.question.hidden_by = $window.user_id;
                        // $scope.question.hidden_justification = $scope.question.hidden_justification;
                        // $modalInstance.close($scope.question);
                    };

                    $scope.cancel = function () {
                        $modalInstance.dismiss();
                    };
                };

                $scope.new_message = function () {
                    var modalInstance = $modal.open({
                        templateUrl: 'newMessageModal.html',
                        controller: SendMessageModalInstanceCtrl,
                        // resolve: {
                            // users: function () {
                                // return question;
                            // }
                        // }
                    });

                    modalInstance.result.then(function (question) {
                        question.$update({questionId: question.id}, function(question){
                            question.hidden_to_user = false;
                        });
                        
                    });
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
                        }
                        index++;
                    });
                    var bla = 0;
                });
            }
        ]);
})(angular);
