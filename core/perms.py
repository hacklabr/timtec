from permission.logics.groupin import GroupInPermissionLogic

PERMISSION_LOGICS = (
    ('core.Course', GroupInPermissionLogic('groups', any_permission=False)),
)
