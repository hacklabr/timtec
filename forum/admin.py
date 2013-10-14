# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from suit.admin import SortableTabularInline

from models import Question, Answer, AnswerVote, QuestionVote


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'class': 'span12'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'class': 'span12'})},
    }


class QuestionVoteInline(SortableTabularInline):
    model = QuestionVote
    sortable = 'id'


class AnswerVoteInline(SortableTabularInline):
    model = AnswerVote
    sortable = 'id'


class AnswerInline(SortableTabularInline):
    model = Answer
    sortable = 'id'


class QuestionAdmin(ModelAdmin):
    inlines = (AnswerInline, QuestionVoteInline)


class AnswerAdmin(ModelAdmin):
    inlines = (AnswerVoteInline,)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
