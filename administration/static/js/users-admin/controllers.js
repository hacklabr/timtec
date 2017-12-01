(function(angular){

    var app = angular.module('users-admin.controllers', []);

    app.controller('UsersAdminController', ['$scope', '$window', '$uibModal', '$http', '$q',  'UserAdmin',
        function($scope, $window,$uibModal, $http, $q, UserAdmin) {

            var success_save_msg = 'Alterações salvas com sucesso.';
            var error_save_msg = 'Não foi possível salvar as alterações.';

            var confirm_delete_user_msg = 'Tem certeza que deseja apagar este usuário? Esta operação não poderá ser desfeita!';
            var success_delete_user_msg = 'Usuário apagado com sucesso.';
            var error_delete_user_msg = 'Erro ao apagar usuário.';

            $scope.total_users_found = parseInt($window.total_users_found, 10);

            $scope.users_page = UserAdmin.query({page: 1});

            $scope.filters = {};

            $scope.clean_groups = function(groups){
              // "students" group must be ommited
              for (var i = 0; i < groups.length; i++) {
                  if(groups[i].name === "students"){
                      groups.splice(i, 1);
                      i = -1;  // if an element has been removed, the counter is outdated and must be reinitialized
                  }
              }
            };

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


    app.controller('GroupAdminController', ['$scope', '$window', '$uibModal', '$http', '$q', 'Contracts', 'GroupAdmin', 'UserAdmin',
        function($scope, $window,$uibModal, $http, $q, Contracts, GroupAdmin, UserAdmin) {

            var success_create_group_msg = 'Grupo criado com sucesso.';
            var success_delete_group_msg = 'Grupo apagado com sucesso.';
            var success_user_add = 'Usuários adicionados ao grupo com sucesso.'
            var success_user_rmv = 'Usuário removido do grupo com sucesso.';
            var success_users_rmv = 'Usuários removidos do grupo com sucesso.';
            var error_user_rmv = 'Erro ao remover usuário do grupo.';
            var error_users_rmv = 'Erro ao remover usuários do grupo';

            // region Contracts
            $scope.contracts = Contracts.query();
            $scope.contract = '';

            $scope.filter_contracts = function() {
                if ($scope.contract == 0) {
                    $scope.groups.filtered = $scope.groups.all;
                }
                else {
                    $scope.groups.filtered = $scope.groups.all.filter(function(group) {
                        return group.contract && group.contract.id == $scope.contract;
                    });
                }
            };
            // endregion Contracts

            // region Contracts
            $scope.contracts = Contracts.query();
            $scope.contract = '';

            $scope.filter_contracts = function() {
                if ($scope.contract == 0) {
                    $scope.groups.filtered = $scope.groups.all;
                }
                else {
                    $scope.groups.filtered = $scope.groups.all.filter(function(group) {
                        return group.contract && group.contract.id == $scope.contract;
                    });
                }
            };
            // endregion Contracts

            var reload_groups = function(message){
                GroupAdmin.query(function(groups){
                    // "students" and "professros" groups must be ommited
                    // for (var i = 0; i < groups.length; i++) {
                    //     if(groups[i].name === "students" || groups[i].name === "professors"){
                    //         groups.splice(i, 1);
                    //         i = -1;  // if an element has been removed, the counter is outdated and must be reinitialized
                    //     }
                    // }
                    $scope.groups = {};
                    $scope.groups.all = groups;
                    $scope.groups.filtered = $scope.groups.all;
                    if (message !== undefined){
                        $scope.alert.success(message);
                    }
                });
            };
            reload_groups();  // initial groups load

            $scope.remove_user = function(group, user) {
                GroupAdmin.update({id: group.id, user: user, action: "remove"}, function() {
                    reload_groups(success_user_rmv);
                }, function() {
                    $scope.alert.error(error_user_rmv);
                });
            };

            $scope.remove_group = function (group) {
                if (window.confirm('Deseja mesmo remover o grupo?')){
                    GroupAdmin.delete({id: group.id}, function(){
                        reload_groups(success_delete_group_msg);
                    });
                }
            };

            // Add new users to a group using a modal
            $scope.new_group = function () {
                var modalInstance = $uibModal.open({
                    templateUrl: 'newGroupModal.html',
                    controller: ['$scope', '$uibModalInstance', addGroupModalInstanceCtrl],
                });
            };
            var addGroupModalInstanceCtrl = function ($scope, $uibModalInstance) {
                $scope.add_group = function () {
                    GroupAdmin.save({name: $scope.group_name}, function(){
                        reload_groups(success_create_group_msg);
                    });
                    $uibModalInstance.close();
                };

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };
            };

            // Add new users to a group using a modal
            $scope.new_users = function (group) {
                var modalInstance = $uibModal.open({
                    templateUrl: 'newUserModal.html',
                    controller: ['$scope', '$uibModalInstance', 'group', addUserModalInstanceCtrl],
                    resolve: {
                        group: function () {
                            return group;
                        }
                    }
                });
            };
            var addUserModalInstanceCtrl = function ($scope, $uibModalInstance, group) {

                $scope.group = group;
                $scope.new_users = [];
                $scope.add_professors = function () {
                    GroupAdmin.update({id: group.id, users: $scope.new_users, action: "add"}, function(){
                        reload_groups(success_user_add);
                    });
                    $uibModalInstance.close();
                };

                $scope.cancel = function () {
                    $uibModalInstance.dismiss();
                };

                $scope.on_select_professor = function(model) {
                    $scope.new_users.unshift(model);
                    $scope.asyncSelected = '';
                };

                $scope.remove_new_professor = function(index) {
                    $scope.new_users.splice(index, 1);
                };

                $scope.getUsers = function(val) {
                    return $http.get('/api/user_search', {
                        params: {
                          name: val,
                          sensor: false
                        }
                    }).then(function(res){
                        var professors_found = [];
                        angular.forEach(res.data, function(item){
                            var formated_name = '';
                            if (item.first_name)
                                formated_name += item.first_name;
                            if (item.last_name)
                                formated_name = formated_name + ' ' + item.last_name;
                            if (formated_name)
                                formated_name = formated_name + ' - ';
                            formated_name += item.username;
                            if (item.email)
                                formated_name = formated_name + ' - ' + item.email;
                            item.formated_name = formated_name;
                            professors_found.push(item);
                        });
                        return professors_found;
                    });
                };

                $scope.bulk_add = function() {
                    var emails_array = $scope.bulk_add_list.split(/\n/);
                    GroupAdmin.update({id: group.id, users: emails_array, action: "bulk_add"}, function(data) {
                        reload_groups(success_user_add);
                    }, function(error) {
                        $scope.alert.error(error_user_add);
                    });
                    $uibModalInstance.close();
                };
            };

            // Bulk removal of users to a group using a modal
            $scope.remove_users = function(group) {
                var modalInstance = $uibModal.open({
                    templateUrl: 'removeUsersModal.html',
                    controller: ['$scope', '$uibModalInstance', 'group', removeUsersModalInstanceCtrl],
                    resolve: {
                        group: function() {
                            return group;
                        }
                    }
                });
            }
            var removeUsersModalInstanceCtrl = function($scope, $uibModalInstance, group) {
                $scope.group = group;

                $scope.cancel = function() {
                    $uibModalInstance.dismiss();
                };

                $scope.bulk_remove = function() {
                    var emails_array = $scope.bulk_remove_list.split(/\n/);
                    GroupAdmin.update({id: group.id, users: emails_array, action: "bulk_remove"}, function(data) {
                        reload_groups(success_user_rmv);
                    }, function(error) {
                        $scope.alert.error(error_user_rmv);
                    });
                    $uibModalInstance.close();
                };
            }
        }
    ]);

})(angular);
