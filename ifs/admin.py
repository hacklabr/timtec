from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Campus

User = get_user_model()


class IfUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('ifid', 'campus', 'city', 'course', 'klass', 'is_if_staff', 'cpf', 'siape',)}),
    )

admin.site.unregister(User)

admin.site.register(User, IfUserAdmin)
admin.site.register(Campus)
