from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TimtecUser

admin.site.register(TimtecUser, UserAdmin)
