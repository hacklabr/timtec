(function(angular){

    angular.module('users-admin.controllers', []).
        controller('UsersAdminController', ['$scope', '$window', '$modal', '$http', '$q',  'UserAdmin',
        function($scope, $window, $modal, $http, $q, UserAdmin) {

            var success_save_msg = 'Alterações salvas com sucesso.';
            var error_save_msg = 'Não foi possível salvar as alterações.';

            var confirm_delete_user_msg = 'Tem certeza que deseja apagar este usuário? Esta operação não poderá ser desfeita!';
            var success_delete_user_msg = 'Usuário apagado com sucesso.';
            var error_delete_user_msg = 'Erro ao apagar usuário.';

            $scope.total_users_found = parseInt($window.total_users_found, 10);

            $scope.users_page = UserAdmin.query({page: 1});

            $scope.filters = {};

            $scope.filter_users = function() {
                $scope.users_page = UserAdmin.query($scope.filters, function(users_page) {
                    $scope.filtered = true;
                    $scope.total_users_found = users_page.length;
                });
            };

            $scope.page_changed = function() {
                $scope.users_page = UserAdmin.query({page: $scope.current_page});
            };

            $scope.update_user = function(user) {
                user.$update({user_id: user.id}, function() {
                    $scope.alert.success(success_save_msg);
                }, function() {
                    $scope.alert.error(error_save_msg);
                });
            };

            $scope.delete_user = function(user, index) {
                if (confirm(confirm_delete_user_msg)) {
                    user.$remove({user_id: user.id}, function() {
                        $scope.users_page.splice(index, 1);
                        $scope.alert.success(success_delete_user_msg);
                    }, function() {
                        $scope.alert.error(error_delete_user_msg);
                    });
                }
            };
        }
    ]);

})(angular);
