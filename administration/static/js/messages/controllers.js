(function(angular){

    angular.module('messages.controllers', []).
        controller('MessagesManagerController', ['$scope', '$modal', 'Message', 'User',
            function($scope, $modal,  Message, User) {
                var course_id = document.location.href.match(/course\/([0-9]+)/)[1];
                $scope.messages = Message.query({course: course_id});


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

                $scope.new_message = function (question) {
                    var modalInstance = $modal.open({
                        templateUrl: 'newMessageModal.html',
                        controller: SendMessageModalInstanceCtrl,
                        // resolve: {
                            // question: function () {
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
        controller('MessageController', ['$scope', 'Message', 'User',
            function($scope,  Message, User) {
            }
        ]);
})(angular);
