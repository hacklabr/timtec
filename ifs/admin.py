from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

TimtecUser = get_user_model()


class MyUserAdmin(UserAdmin):
    model = TimtecUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('ifid', 'campus', 'city', 'course', 'klass')}),
    )

admin.site.unregister(TimtecUser)
admin.site.register(TimtecUser, MyUserAdmin)
