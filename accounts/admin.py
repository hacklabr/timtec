from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class TimtecUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (_('Timtec Info'), {'fields': ('accepted_terms', 'picture', 'cpf')}),
    )

admin.site.register(User, TimtecUserAdmin)
