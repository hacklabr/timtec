from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class IfUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('ifid', 'campus', 'city', 'course', 'klass', 'is_if_staff',)}),
    )

admin.site.unregister(User)

admin.site.register(User, IfUserAdmin)
