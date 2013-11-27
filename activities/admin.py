from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import Answer, Activity


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'class': 'span12'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'class': 'span12'})},
    }


class ActivityAdmin(ModelAdmin):
    list_display = ('type', 'question', '__unicode__',)


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Answer)
